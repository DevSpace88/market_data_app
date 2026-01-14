"""
Authentication API routes.

Supports both Authorization header and httpOnly cookie authentication.
"""
import re
import logging
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...models.database import get_db
from ...models.user import User
from ...schemas.user import UserCreate, UserResponse, UserUpdate
from ...auth import (
    Token,
    create_access_token,
    get_current_active_user,
    set_auth_cookie,
    clear_auth_cookie,
)
from ...config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()
router = APIRouter()


def validate_email(email: str) -> bool:
    """Simple email validation"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Validate email format
    if not validate_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Check if username already exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email already exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=User.get_password_hash(user_data.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    logger.info(f"New user registered: {db_user.username}")
    return db_user


@router.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login a user and set httpOnly cookie with access token"""

    # Find user by username
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user must change password
    if user.must_change_password:
        logger.info(f"User {user.username} must change default password")

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    # Set httpOnly cookie
    set_auth_cookie(response, access_token)

    logger.info(f"User logged in: {user.username}")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user),
        "must_change_password": user.must_change_password
    }


@router.post("/logout")
async def logout(response: Response):
    """Clear authentication cookie"""
    clear_auth_cookie(response)
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return UserResponse.model_validate(current_user)


@router.get("/validate-token")
async def validate_token(current_user: User = Depends(get_current_active_user)):
    """Validate user token and return user info"""
    return {
        "valid": True,
        "user": UserResponse.model_validate(current_user)
    }


@router.put("/me", response_model=UserResponse)
async def update_user_info(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user information"""
    # Check email if provided
    if user_data.email and user_data.email != current_user.email:
        if not validate_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = user_data.email

    # Update other fields
    if user_data.full_name is not None:
        current_user.full_name = user_data.full_name
    if user_data.password:
        current_user.hashed_password = User.get_password_hash(user_data.password)
        # Clear must_change_password flag if user is changing password
        current_user.must_change_password = False

    db.commit()
    db.refresh(current_user)

    logger.info(f"User updated profile: {current_user.username}")
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """OAuth2 compatible token login for Swagger UI.

    Sets both cookie and returns token for backward compatibility.
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    # Set httpOnly cookie
    set_auth_cookie(response, access_token)

    logger.info(f"OAuth2 token login: {user.username}")

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
