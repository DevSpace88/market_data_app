from fastapi import Depends, HTTPException, status, WebSocket
from fastapi.security import OAuth2PasswordBearer
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
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}/auth/token",
    scheme_name="JWT"
)

# Pydantic Models für Auth
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

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

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# WebSocket auth
async def get_token_from_ws_query(websocket: WebSocket) -> Optional[str]:
    return websocket.query_params.get("token")

async def verify_ws_token(token: str, db: Session = Depends(get_db)) -> Optional[User]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            return None

        user = db.query(User).filter(User.username == username).first()
        return user
    except DecodeError:  # Changed from JWTDecodeError
        return None