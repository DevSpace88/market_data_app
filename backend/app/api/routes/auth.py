# # # # # # # app/api/routes/auth.py
# # # # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # # # from fastapi.security import OAuth2PasswordRequestForm
# # # # # # from datetime import timedelta
# # # # # # from ...auth import Token, User, create_access_token, get_user, verify_password, fake_users_db, get_current_active_user
# # # # # # from ...config import get_settings
# # # # # #
# # # # # # settings = get_settings()
# # # # # # router = APIRouter()
# # # # # #
# # # # # #
# # # # # # @router.post("/token", response_model=Token)
# # # # # # async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
# # # # # #     user = get_user(fake_users_db, form_data.username)
# # # # # #     if not user or not verify_password(form_data.password, user.hashed_password):
# # # # # #         raise HTTPException(
# # # # # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # # # # #             detail="Incorrect username or password",
# # # # # #             headers={"WWW-Authenticate": "Bearer"},
# # # # # #         )
# # # # # #     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
# # # # # #     access_token = create_access_token(
# # # # # #         data={"sub": user.username}, expires_delta=access_token_expires
# # # # # #     )
# # # # # #     return {"access_token": access_token, "token_type": "bearer"}
# # # # # #
# # # # # #
# # # # # # @router.get("/users/me", response_model=User)
# # # # # # async def read_users_me(current_user: User = Depends(get_current_active_user)):
# # # # # #     return current_user
# # # # # #
# # # # # #
# # # # # # app/api/routes/auth.py
# # # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # # from fastapi.security import OAuth2PasswordRequestForm
# # # # # from datetime import timedelta  # Dieser Import fehlte
# # # # # from ...auth import (
# # # # #     Token,
# # # # #     User,
# # # # #     create_access_token,
# # # # #     get_user,
# # # # #     verify_password,
# # # # #     fake_users_db,
# # # # #     get_current_active_user
# # # # # )
# # # # # from ...config import get_settings
# # # # #
# # # # # settings = get_settings()
# # # # # router = APIRouter()
# # # # #
# # # # #
# # # # # @router.post("/token", response_model=Token)
# # # # # async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
# # # # #     print(f"Login attempt for user: {form_data.username}")
# # # # #
# # # # #     user = get_user(fake_users_db, form_data.username)
# # # # #     if not user:
# # # # #         print(f"User not found: {form_data.username}")
# # # # #         raise HTTPException(
# # # # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # # # #             detail="Incorrect username or password",
# # # # #             headers={"WWW-Authenticate": "Bearer"},
# # # # #         )
# # # # #
# # # # #     if not verify_password(form_data.password, user.hashed_password):
# # # # #         print(f"Invalid password for user: {form_data.username}")
# # # # #         raise HTTPException(
# # # # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # # # #             detail="Incorrect username or password",
# # # # #             headers={"WWW-Authenticate": "Bearer"},
# # # # #         )
# # # # #
# # # # #     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
# # # # #     access_token = create_access_token(
# # # # #         data={"sub": user.username}, expires_delta=access_token_expires
# # # # #     )
# # # # #
# # # # #     print(f"Login successful for user: {form_data.username}")
# # # # #     return {"access_token": access_token, "token_type": "bearer"}
# # # # #
# # # # #
# # # # # @router.get("/users/me", response_model=User)
# # # # # async def read_users_me(current_user: User = Depends(get_current_active_user)):
# # # # #     return current_user
# # # # #
# # # # #
# # # # # @router.get("/test-auth")
# # # # # async def test_auth(current_user: User = Depends(get_current_active_user)):
# # # # #     return {
# # # # #         "message": "Authentication successful",
# # # # #         "user": current_user.username
# # # # #     }
# # # #
# # # # # app/api/routes/auth.py
# # # # from fastapi import APIRouter, Depends, HTTPException, status, Response
# # # # from fastapi.security import OAuth2PasswordRequestForm
# # # # from fastapi.responses import JSONResponse
# # # # from datetime import timedelta
# # # # import logging
# # # # from ...auth import (
# # # #     Token,
# # # #     User,
# # # #     create_access_token,
# # # #     get_user,
# # # #     verify_password,
# # # #     fake_users_db,
# # # #     get_current_active_user
# # # # )
# # # # from ...config import get_settings
# # # #
# # # # logger = logging.getLogger(__name__)
# # # # settings = get_settings()
# # # # router = APIRouter()
# # # #
# # # #
# # # # @router.post("/token")
# # # # async def login_for_access_token(
# # # #         response: Response,
# # # #         form_data: OAuth2PasswordRequestForm = Depends()
# # # # ):
# # # #     logger.debug(f"Login attempt for user: {form_data.username}")
# # # #
# # # #     try:
# # # #         user = get_user(fake_users_db, form_data.username)
# # # #         if not user:
# # # #             logger.warning(f"User not found: {form_data.username}")
# # # #             return JSONResponse(
# # # #                 status_code=status.HTTP_401_UNAUTHORIZED,
# # # #                 content={
# # # #                     "detail": "Incorrect username or password"
# # # #                 },
# # # #                 headers={"WWW-Authenticate": "Bearer"}
# # # #             )
# # # #
# # # #         if not verify_password(form_data.password, user.hashed_password):
# # # #             logger.warning(f"Invalid password for user: {form_data.username}")
# # # #             return JSONResponse(
# # # #                 status_code=status.HTTP_401_UNAUTHORIZED,
# # # #                 content={
# # # #                     "detail": "Incorrect username or password"
# # # #                 },
# # # #                 headers={"WWW-Authenticate": "Bearer"}
# # # #             )
# # # #
# # # #         access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
# # # #         access_token = create_access_token(
# # # #             data={"sub": user.username}, expires_delta=access_token_expires
# # # #         )
# # # #
# # # #         logger.info(f"Login successful for user: {form_data.username}")
# # # #         return {"access_token": access_token, "token_type": "bearer"}
# # # #
# # # #     except Exception as e:
# # # #         logger.error(f"Login error: {str(e)}", exc_info=True)
# # # #         return JSONResponse(
# # # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # # #             content={"detail": "Internal server error during authentication"}
# # # #         )
# # # #
# # # #
# # # # @router.get("/users/me", response_model=User)
# # # # async def read_users_me(current_user: User = Depends(get_current_active_user)):
# # # #     return current_user
# # # #
# # # #
# # # # @router.get("/test")
# # # # async def test_auth(current_user: User = Depends(get_current_active_user)):
# # # #     """Test route to verify authentication is working"""
# # # #     return {
# # # #         "message": "Authentication successful",
# # # #         "user": current_user.username
# # # #     }
# # #
# # # # app/api/routes/auth.py
# # # from fastapi import APIRouter, Depends, HTTPException, status
# # # from fastapi.security import OAuth2PasswordRequestForm
# # # from pydantic import BaseModel, EmailStr
# # # from typing import Optional
# # # from datetime import timedelta
# # #
# # # from ...auth import (
# # #     Token,
# # #     User,
# # #     create_access_token,
# # #     get_user,
# # #     verify_password,
# # #     fake_users_db,
# # #     get_current_active_user,
# # #     get_password_hash
# # # )
# # # from ...config import get_settings
# # #
# # # settings = get_settings()
# # # router = APIRouter()
# # #
# # #
# # # class UserRegister(BaseModel):
# # #     username: str
# # #     email: EmailStr
# # #     password: str
# # #     full_name: Optional[str] = None
# # #
# # #
# # # class UserResponse(BaseModel):
# # #     username: str
# # #     email: str
# # #     full_name: Optional[str] = None
# # #
# # #
# # # class LoginResponse(BaseModel):
# # #     access_token: str
# # #     token_type: str
# # #     user: UserResponse
# # #
# # #
# # # @router.post("/register", response_model=UserResponse)
# # # async def register(user_data: UserRegister):
# # #     if user_data.username in fake_users_db:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_400_BAD_REQUEST,
# # #             detail="Username already registered"
# # #         )
# # #
# # #     user_dict = {
# # #         "username": user_data.username,
# # #         "email": user_data.email,
# # #         "full_name": user_data.full_name,
# # #         "hashed_password": get_password_hash(user_data.password),
# # #         "disabled": False
# # #     }
# # #
# # #     fake_users_db[user_data.username] = user_dict
# # #     return UserResponse(**user_dict)
# # #
# # #
# # # @router.post("/login", response_model=LoginResponse)
# # # async def login(form_data: OAuth2PasswordRequestForm = Depends()):
# # #     user = get_user(fake_users_db, form_data.username)
# # #     if not user or not verify_password(form_data.password, user.hashed_password):
# # #         raise HTTPException(
# # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # #             detail="Incorrect username or password",
# # #             headers={"WWW-Authenticate": "Bearer"},
# # #         )
# # #
# # #     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
# # #     access_token = create_access_token(
# # #         data={"sub": user.username},
# # #         expires_delta=access_token_expires
# # #     )
# # #
# # #     return {
# # #         "access_token": access_token,
# # #         "token_type": "bearer",
# # #         "user": UserResponse(
# # #             username=user.username,
# # #             email=user.email,
# # #             full_name=user.full_name
# # #         )
# # #     }
# # #
# # #
# # # @router.get("/me", response_model=UserResponse)
# # # async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
# # #     return UserResponse(
# # #         username=current_user.username,
# # #         email=current_user.email,
# # #         full_name=current_user.full_name
# # #     )
# #
# #
# # # app/api/routes/auth.py
# # from fastapi import APIRouter, Depends, HTTPException, status
# # from fastapi.security import OAuth2PasswordRequestForm
# # from fastapi.responses import JSONResponse
# # from pydantic import BaseModel, EmailStr
# # from typing import Optional
# # from datetime import timedelta
# # from ...auth import (
# #     Token,
# #     User,
# #     create_access_token,
# #     get_user,
# #     verify_password,
# #     fake_users_db,
# #     get_current_active_user,
# #     get_password_hash
# # )
# # from ...config import get_settings
# #
# # settings = get_settings()
# # router = APIRouter()
# #
# #
# # class UserRegister(BaseModel):
# #     username: str
# #     email: EmailStr
# #     password: str
# #     full_name: Optional[str] = None
# #
# #
# # class UserResponse(BaseModel):
# #     username: str
# #     email: str
# #     full_name: Optional[str] = None
# #
# #
# # class LoginResponse(BaseModel):
# #     access_token: str
# #     token_type: str
# #     user: UserResponse
# #
# #
# # @router.post("/register", response_model=UserResponse)
# # async def register(user_data: UserRegister):
# #     if user_data.username in fake_users_db:
# #         raise HTTPException(
# #             status_code=status.HTTP_400_BAD_REQUEST,
# #             detail="Username already registered"
# #         )
# #
# #     user_dict = {
# #         "username": user_data.username,
# #         "email": user_data.email,
# #         "full_name": user_data.full_name,
# #         "hashed_password": get_password_hash(user_data.password),
# #         "disabled": False
# #     }
# #
# #     fake_users_db[user_data.username] = user_dict
# #     return UserResponse(**user_dict)
# #
# #
# # # Diese Route ist für die normale Login-API
# # @router.post("/login", response_model=LoginResponse)
# # async def login(form_data: OAuth2PasswordRequestForm = Depends()):
# #     user = get_user(fake_users_db, form_data.username)
# #     if not user or not verify_password(form_data.password, user.hashed_password):
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Incorrect username or password",
# #             headers={"WWW-Authenticate": "Bearer"},
# #         )
# #
# #     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
# #     access_token = create_access_token(
# #         data={"sub": user.username},
# #         expires_delta=access_token_expires
# #     )
# #
# #     return {
# #         "access_token": access_token,
# #         "token_type": "bearer",
# #         "user": UserResponse(
# #             username=user.username,
# #             email=user.email,
# #             full_name=user.full_name
# #         )
# #     }
# #
# #
# # # Diese Route ist für Swagger UI Auth
# # @router.post("/token", response_model=Token)
# # async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
# #     user = get_user(fake_users_db, form_data.username)
# #     if not user or not verify_password(form_data.password, user.hashed_password):
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Incorrect username or password",
# #             headers={"WWW-Authenticate": "Bearer"},
# #         )
# #
# #     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
# #     access_token = create_access_token(
# #         data={"sub": user.username},
# #         expires_delta=access_token_expires
# #     )
# #
# #     return {
# #         "access_token": access_token,
# #         "token_type": "bearer"
# #     }
# #
# #
# # # @router.get("/me", response_model=UserResponse)
# # # async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
# # #     return UserResponse(
# # #         username=current_user.username,
# # #         email=current_user.email,
# # #         full_name=current_user.full_name
# # #     )
# #
# #
# # @router.get("/me", response_model=UserResponse)
# # async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
# #     try:
# #         return UserResponse(
# #             username=current_user.username,
# #             email=current_user.email,
# #             full_name=current_user.full_name
# #         )
# #     except Exception as e:
# #         return JSONResponse(
# #             status_code=500,
# #             content={
# #                 "error": "Failed to get user info",
# #                 "detail": str(e)
# #             }
# #         )
# #
# # @router.get("/whoami")
# # async def whoami(current_user: User = Depends(get_current_active_user)):
# #     return JSONResponse(
# #         status_code=200,
# #         content={
# #             "username": current_user.username,
# #             "email": current_user.email,
# #             "full_name": current_user.full_name
# #         }
# #     )
#
#
#
#
# # app/api/routes/auth.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from datetime import timedelta
# import re
# from typing import Optional
# from ...models.database import get_db
# from ...models.user import User
# from ...schemas.user import UserCreate, UserResponse
# from ...auth import create_access_token, get_current_active_user
# from ...config import get_settings
#
# settings = get_settings()
# router = APIRouter()
#
#
# def validate_email(email: str) -> bool:
#     """Simple email validation"""
#     pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
#     return bool(re.match(pattern, email))
#
#
# @router.post("/register", response_model=UserResponse)
# async def register(
#         user_data: UserCreate,
#         db: Session = Depends(get_db)
# ):
#     # Validiere Email
#     if not validate_email(user_data.email):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid email format"
#         )
#
#     # Prüfe ob User existiert
#     if db.query(User).filter(User.username == user_data.username).first():
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Username already registered"
#         )
#
#     if db.query(User).filter(User.email == user_data.email).first():
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already registered"
#         )
#
#     # Erstelle neuen User
#     db_user = User(
#         username=user_data.username,
#         email=user_data.email,
#         full_name=user_data.full_name,
#         hashed_password=User.get_password_hash(user_data.password)
#     )
#
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#
#     return db_user
#
#
# @router.post("/login")
# async def login(
#         form_data: OAuth2PasswordRequestForm = Depends(),
#         db: Session = Depends(get_db)
# ):
#     # Finde User
#     user = db.query(User).filter(User.username == form_data.username).first()
#     if not user or not user.verify_password(form_data.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username},
#         expires_delta=access_token_expires
#     )
#
#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#         "user": UserResponse.model_validate(user)
#     }
#
#
# @router.get("/me", response_model=UserResponse)
# async def get_current_user(current_user: User = Depends(get_current_active_user)):
#     return current_user
#
#
# @router.get("/validate-token")
# async def validate_token(current_user: User = Depends(get_current_active_user)):
#     return {"valid": True, "user": UserResponse.model_validate(current_user)}

# api/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import re
from fastapi.responses import JSONResponse
from typing import Optional

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import re

from ...models.database import get_db
from ...models.user import User
from ...schemas.user import UserCreate, UserResponse, UserUpdate
from ...auth import Token, create_access_token, get_current_active_user  # Korrigierter Import
from ...config import get_settings

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

    return db_user

@router.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """Login a user and return access token"""
    logger.debug(f"Login attempt for username: {form_data.username}")

    # Find user by username
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    logger.debug(f"Login successful for user: {user.username}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    logger.debug(f"Received request for user info with token")
    logger.debug(f"Current user: {current_user.username}")
    try:
        response = UserResponse.model_validate(current_user)
        logger.debug(f"Response prepared: {response}")
        return response
    except Exception as e:
        logger.error(f"Error in get_current_user_info: {str(e)}")
        raise
@router.get("/validate-token")
async def validate_token(current_user: User = Depends(get_current_active_user)):
    """Validate user token and return user info"""
    return {"valid": True, "user": UserResponse.model_validate(current_user)}


# Optional: Update user endpoint
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

    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """OAuth2 compatible token login for Swagger UI."""
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

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }