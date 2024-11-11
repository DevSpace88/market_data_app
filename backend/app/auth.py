# # # app/auth.py
# # from fastapi import Depends, HTTPException, status, WebSocket
# # from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# # from jose import JWTError, jwt
# # from passlib.context import CryptContext
# # from datetime import datetime, timedelta
# # from typing import Optional, Dict
# # from pydantic import BaseModel
# # from .config import get_settings
# #
# # settings = get_settings()
# #
# #
# # # Pydantic Models
# # class Token(BaseModel):
# #     access_token: str
# #     token_type: str
# #
# #
# # class TokenData(BaseModel):
# #     username: Optional[str] = None
# #
# #
# # class User(BaseModel):
# #     username: str
# #     email: Optional[str] = None
# #     full_name: Optional[str] = None
# #     disabled: Optional[bool] = None
# #
# #
# # class UserInDB(User):
# #     hashed_password: str
# #
# #
# # # Auth Configuration
# # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# # oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/token")
# #
# #
# # # Helper Functions
# # def verify_password(plain_password, hashed_password):
# #     return pwd_context.verify(plain_password, hashed_password)
# #
# #
# # def get_password_hash(password):
# #     return pwd_context.hash(password)
# #
# #
# # def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
# #     to_encode = data.copy()
# #     if expires_delta:
# #         expire = datetime.utcnow() + expires_delta
# #     else:
# #         expire = datetime.utcnow() + timedelta(minutes=15)
# #     to_encode.update({"exp": expire})
# #     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
# #     return encoded_jwt
# #
# #
# # # Dummy DB - Replace with your database logic
# # fake_users_db = {
# #     "testuser": {
# #         "username": "testuser",
# #         "full_name": "Test User",
# #         "email": "test@example.com",
# #         "hashed_password": get_password_hash("testpassword"),
# #         "disabled": False,
# #     }
# # }
# #
# #
# # def get_user(db, username: str):
# #     if username in db:
# #         user_dict = db[username]
# #         return UserInDB(**user_dict)
# #
# #
# # async def get_current_user(token: str = Depends(oauth2_scheme)):
# #     credentials_exception = HTTPException(
# #         status_code=status.HTTP_401_UNAUTHORIZED,
# #         detail="Could not validate credentials",
# #         headers={"WWW-Authenticate": "Bearer"},
# #     )
# #     try:
# #         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
# #         username: str = payload.get("sub")
# #         if username is None:
# #             raise credentials_exception
# #         token_data = TokenData(username=username)
# #     except JWTError:
# #         raise credentials_exception
# #     user = get_user(fake_users_db, username=token_data.username)
# #     if user is None:
# #         raise credentials_exception
# #     return user
# #
# #
# # async def get_current_active_user(current_user: User = Depends(get_current_user)):
# #     if current_user.disabled:
# #         raise HTTPException(status_code=400, detail="Inactive user")
# #     return current_user
# #
# #
# # # WebSocket Auth
# # async def get_token_from_ws_query(websocket: WebSocket) -> Optional[str]:
# #     """Extract token from WebSocket query parameters"""
# #     token = websocket.query_params.get("token")
# #     return token
# #
# #
# # async def verify_ws_token(token: str) -> Optional[User]:
# #     """Verify WebSocket token and return user"""
# #     try:
# #         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
# #         username: str = payload.get("sub")
# #         if username is None:
# #             return None
# #         user = get_user(fake_users_db, username=username)
# #         return user
# #     except JWTError:
# #         return None
# #
# #
#
#
# # # app/auth.py
# # from fastapi import Depends, HTTPException, status, WebSocket
# # from fastapi.security import OAuth2PasswordBearer
# # from jose import JWTError, jwt
# # from passlib.context import CryptContext
# # from datetime import datetime, timedelta
# # from typing import Optional
# # from pydantic import BaseModel
# # from .config import get_settings
# #
# # settings = get_settings()
# #
# # # Pydantic Models
# # class Token(BaseModel):
# #     access_token: str
# #     token_type: str
# #
# # class TokenData(BaseModel):
# #     username: Optional[str] = None
# #
# # class User(BaseModel):
# #     username: str
# #     email: Optional[str] = None
# #     full_name: Optional[str] = None
# #     disabled: Optional[bool] = None
# #
# # class UserInDB(User):
# #     hashed_password: str
# #
# # # Auth Configuration
# # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# # oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/token")
# #
# #
# # async def get_current_user(token: str = Depends(oauth2_scheme)):
# #     credentials_exception = HTTPException(
# #         status_code=status.HTTP_401_UNAUTHORIZED,
# #         detail="Could not validate credentials",
# #         headers={"WWW-Authenticate": "Bearer"},
# #     )
# #     try:
# #         # Hier ist die Korrektur für das JWT Decode
# #         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
# #         username: str = payload.get("sub")
# #         if username is None:
# #             raise credentials_exception
# #         token_data = TokenData(username=username)
# #     except JWTError:
# #         raise credentials_exception
# #
# #     user = get_user(fake_users_db, username=token_data.username)
# #     if user is None:
# #         raise credentials_exception
# #     return user
# #
# #
# # # Helper Functions
# # def verify_password(plain_password, hashed_password):
# #     return pwd_context.verify(plain_password, hashed_password)
# #
# # def get_password_hash(password):
# #     return pwd_context.hash(password)
# #
# # # Dummy DB - Replace with your database logic
# # fake_users_db = {
# #     "testuser": {
# #         "username": "testuser",
# #         "full_name": "Test User",
# #         "email": "test@example.com",
# #         "hashed_password": pwd_context.hash("testpass"),
# #         "disabled": False,
# #     }
# # }
# #
# # def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
# #     to_encode = data.copy()
# #     if expires_delta:
# #         expire = datetime.utcnow() + expires_delta
# #     else:
# #         expire = datetime.utcnow() + timedelta(minutes=15)
# #     to_encode.update({"exp": expire})
# #     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
# #     return encoded_jwt
# #
# # def get_user(db, username: str):
# #     if username in db:
# #         user_dict = db[username]
# #         return UserInDB(**user_dict)
# #
# # # async def get_current_user(token: str = Depends(oauth2_scheme)):
# # #     credentials_exception = HTTPException(
# # #         status_code=status.HTTP_401_UNAUTHORIZED,
# # #         detail="Could not validate credentials",
# # #         headers={"WWW-Authenticate": "Bearer"},
# # #     )
# # #     try:
# # #         payload = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
# # #         username: str = payload.get("sub")
# # #         if username is None:
# # #             raise credentials_exception
# # #         token_data = TokenData(username=username)
# # #     except JWTError:
# # #         raise credentials_exception
# # #     user = get_user(fake_users_db, username=token_data.username)
# # #     if user is None:
# # #         raise credentials_exception
# # #     return user
# #
# # async def get_current_active_user(current_user: User = Depends(get_current_user)):
# #     if current_user.disabled:
# #         raise HTTPException(status_code=400, detail="Inactive user")
# #     return current_user
# #
# # # WebSocket Authentication
# # async def get_token_from_ws_query(websocket: WebSocket) -> Optional[str]:
# #     """Extract token from WebSocket query parameters"""
# #     return websocket.query_params.get("token")
# #
# # async def verify_ws_token(token: str) -> Optional[User]:
# #     """Verify WebSocket token and return user"""
# #     try:
# #         payload = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
# #         username: str = payload.get("sub")
# #         if username is None:
# #             return None
# #         user = get_user(fake_users_db, username=username)
# #         return user
# #     except JWTError:
# #         return None
#
#
# # auth.py
# from fastapi import Depends, HTTPException, status, WebSocket
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from typing import Optional
# from pydantic import BaseModel
# from .config import get_settings
# from .models.database import get_db
# from .models.user import User  # Dein SQLAlchemy User Model
# from sqlalchemy.orm import Session
# import logging
#
# logger = logging.getLogger(__name__)
#
# settings = get_settings()
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# # oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/token")
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl=f"{settings.API_PREFIX}/auth/token",
#     scheme_name="JWT"  # Name in der Swagger UI
# )
#
# async def get_current_user(
#         token: str = Depends(oauth2_scheme),
#         db: Session = Depends(get_db)  # DB Session hinzugefügt
# ):
#     logger.debug("Starting token validation")
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         logger.debug(f"Decoding token: {token[:20]}...")
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         logger.debug(f"Token payload: {payload}")
#
#         username: str = payload.get("sub")
#         if username is None:
#             logger.error("No username in token payload")
#             raise credentials_exception
#
#         # User aus der Datenbank holen statt fake_users_db
#         user = db.query(User).filter(User.username == username).first()
#         if user is None:
#             logger.error(f"No user found in database for username: {username}")
#             raise credentials_exception
#
#         logger.debug(f"User found in database: {user.username}")
#         return user
#
#     except JWTError as e:
#         logger.error(f"JWT Error during validation: {str(e)}")
#         raise credentials_exception
#
#
# async def get_current_active_user(
#         current_user: User = Depends(get_current_user)
# ):
#     logger.debug(f"Checking if user is active: {current_user.username}")
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
#
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     logger.debug(f"Creating access token with data: {data}")
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     logger.debug(f"Token payload before encoding: {to_encode}")
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     logger.debug("Token created successfully")
#     return encoded_jwt
#
#
# # WebSocket Authentication auch anpassen
# async def verify_ws_token(token: str, db: Session = Depends(get_db)) -> Optional[User]:
#     """Verify WebSocket token and return user"""
#     logger.debug("Verifying WS token")
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#         username: str = payload.get("sub")
#         if username is None:
#             logger.error("No username in WS token")
#             return None
#
#         user = db.query(User).filter(User.username == username).first()
#         if not user:
#             logger.error(f"No user found for WS token: {username}")
#             return None
#
#         logger.debug(f"WS token verified for user: {username}")
#         return user
#     except JWTError as e:
#         logger.error(f"WS token verification failed: {str(e)}")
#         return None


# auth.py
from fastapi import Depends, HTTPException, status, WebSocket
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from .models.database import get_db
from .models.user import User
from .config import get_settings
import logging

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
    logger.debug("Starting token validation")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.debug(f"Decoding token: {token[:20]}...")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        logger.debug(f"Token payload: {payload}")

        username: str = payload.get("sub")
        if username is None:
            logger.error("No username in token payload")
            raise credentials_exception

        user = db.query(User).filter(User.username == username).first()
        if user is None:
            logger.error(f"No user found in database for username: {username}")
            raise credentials_exception

        logger.debug(f"User found in database: {user.username}")
        return user

    except JWTError as e:
        logger.error(f"JWT Error during validation: {str(e)}")
        raise credentials_exception


async def get_current_active_user(
        current_user: User = Depends(get_current_user)
):
    logger.debug(f"Checking if user is active: {current_user.username}")
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
):
    """Überprüft ob der User ein Admin ist"""
    logger.debug(f"Checking if user {current_user.username} is admin")
    if not current_user.is_admin:
        logger.warning(f"User {current_user.username} tried to access admin area")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    logger.debug(f"Admin access granted for {current_user.username}")
    return current_user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    logger.debug(f"Creating access token with data: {data}")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    logger.debug(f"Token payload before encoding: {to_encode}")
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    logger.debug("Token created successfully")
    return encoded_jwt


async def get_current_admin_user(
        current_user: User = Depends(get_current_active_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


# WebSocket auth
async def get_token_from_ws_query(websocket: WebSocket) -> Optional[str]:
    return websocket.query_params.get("token")


async def verify_ws_token(token: str, db: Session = Depends(get_db)) -> Optional[User]:
    logger.debug("Verifying WS token")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        username: str = payload.get("sub")
        if not username:
            return None

        user = db.query(User).filter(User.username == username).first()
        return user
    except JWTError:
        return None