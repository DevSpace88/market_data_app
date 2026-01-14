from fastapi import Depends, HTTPException, status, WebSocket, Response
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from .models.database import get_db
from .models.user import User
from .config import get_settings
import logging
import jwt  # Changed from jose
from jwt.exceptions import DecodeError  # Changed from JWTDecodeError

logger = logging.getLogger(__name__)
settings = get_settings()

# Auth configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Support both Authorization header and cookies
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}/auth/token",
    scheme_name="JWT",
    auto_error=False  # Don't raise error if no token, allow cookie fallback
)

# Cookie configuration
AUTH_COOKIE_NAME = "auth_token"
CSRF_COOKIE_NAME = "csrf_token"


class CookieSettings:
    """Configuration for authentication cookies."""
    max_age = 30 * 60  # 30 minutes
    expires = timedelta(minutes=30)
    path = "/"
    domain = None
    secure = False  # Set to True in production with HTTPS
    httponly = True
    samesite = "lax"


cookie_settings = CookieSettings()


# Pydantic Models für Auth
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


def _get_token_from_cookie(request: Request) -> Optional[str]:
    """Extract auth token from httpOnly cookie."""
    return request.cookies.get(AUTH_COOKIE_NAME)


def _get_token_from_header(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[str]:
    """Extract auth token from Authorization header."""
    return token


async def _get_token_optional(
    request: Request,
    header_token: Optional[str] = Depends(_get_token_from_header)
) -> Optional[str]:
    """
    Get token from either header or cookie.
    Priority: header > cookie
    """
    if header_token:
        return header_token
    return _get_token_from_cookie(request)


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    header_token: Optional[str] = Depends(oauth2_scheme)
):
    """
    Get current user from either Authorization header or httpOnly cookie.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Priority: Authorization header > Cookie
    token = header_token
    if not token:
        token = request.cookies.get(AUTH_COOKIE_NAME)
    
    # Debug logging
    header_auth = request.headers.get("Authorization", "")
    cookie_token = request.cookies.get(AUTH_COOKIE_NAME, "")
    logger.info(f"[AUTH DEBUG] Authorization header: {header_auth[:50] if header_auth else 'None'}...")
    logger.info(f"[AUTH DEBUG] Cookie token: {cookie_token[:50] if cookie_token else 'None'}...")
    logger.info(f"[AUTH DEBUG] Final token used: {str(token)[:50] if token else 'None'}...")
    
    if not token:
        logger.debug("No auth token found in header or cookie")
        raise credentials_exception

    try:
        # PyJWT 2.x handles strings correctly
        # Ensure token is a string (not bytes)
        token_str = token if isinstance(token, str) else token.decode('utf-8') if isinstance(token, bytes) else str(token)
        payload = jwt.decode(token_str, settings.auth_secret_key, algorithms=[settings.ALGORITHM])

        username: str = payload.get("sub")
        if username is None:
            logger.error("No username in token payload")
            raise credentials_exception

        user = db.query(User).filter(User.username == username).first()
        if user is None:
            logger.error(f"No user found in database for username: {username}")
            raise credentials_exception

        return user

    except DecodeError as e:  # Changed from JWTDecodeError
        logger.error(f"JWT Error during validation: {str(e)}")
        raise credentials_exception


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
):
    """Überprüft ob der User ein Admin ist"""
    if not current_user.is_admin:
        logger.warning(f"User {current_user.username} tried to access admin area")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.auth_secret_key, algorithm=settings.ALGORITHM)
    return encoded_jwt


def set_auth_cookie(response: Response, token: str) -> None:
    """
    Set httpOnly authentication cookie.

    Args:
        response: FastAPI/Starlette response object
        token: JWT access token
    """
    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=token,
        max_age=cookie_settings.max_age,
        expires=cookie_settings.expires,
        path=cookie_settings.path,
        domain=cookie_settings.domain,
        secure=cookie_settings.secure,
        httponly=cookie_settings.httponly,
        samesite=cookie_settings.samesite,
    )


def clear_auth_cookie(response: Response) -> None:
    """
    Clear authentication cookie.

    Args:
        response: FastAPI/Starlette response object
    """
    response.delete_cookie(
        key=AUTH_COOKIE_NAME,
        path=cookie_settings.path,
        domain=cookie_settings.domain,
    )


# WebSocket auth
async def get_token_from_ws_query(websocket: WebSocket) -> Optional[str]:
    return websocket.query_params.get("token")


async def verify_ws_token(token: str, db: Session = Depends(get_db)) -> Optional[User]:
    try:
        token_str = token if isinstance(token, str) else token.decode('utf-8') if isinstance(token, bytes) else str(token)
        payload = jwt.decode(token_str, settings.auth_secret_key, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            return None

        user = db.query(User).filter(User.username == username).first()
        return user
    except DecodeError:  # Changed from JWTDecodeError
        return None


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response
