# # # app/api/routes/auth.py
# # from fastapi import APIRouter, Depends, HTTPException, status
# # from fastapi.security import OAuth2PasswordRequestForm
# # from datetime import timedelta
# # from ...auth import Token, User, create_access_token, get_user, verify_password, fake_users_db, get_current_active_user
# # from ...config import get_settings
# #
# # settings = get_settings()
# # router = APIRouter()
# #
# #
# # @router.post("/token", response_model=Token)
# # async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
# #     user = get_user(fake_users_db, form_data.username)
# #     if not user or not verify_password(form_data.password, user.hashed_password):
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Incorrect username or password",
# #             headers={"WWW-Authenticate": "Bearer"},
# #         )
# #     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
# #     access_token = create_access_token(
# #         data={"sub": user.username}, expires_delta=access_token_expires
# #     )
# #     return {"access_token": access_token, "token_type": "bearer"}
# #
# #
# # @router.get("/users/me", response_model=User)
# # async def read_users_me(current_user: User = Depends(get_current_active_user)):
# #     return current_user
# #
# #
# # app/api/routes/auth.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from datetime import timedelta  # Dieser Import fehlte
# from ...auth import (
#     Token,
#     User,
#     create_access_token,
#     get_user,
#     verify_password,
#     fake_users_db,
#     get_current_active_user
# )
# from ...config import get_settings
#
# settings = get_settings()
# router = APIRouter()
#
#
# @router.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     print(f"Login attempt for user: {form_data.username}")
#
#     user = get_user(fake_users_db, form_data.username)
#     if not user:
#         print(f"User not found: {form_data.username}")
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     if not verify_password(form_data.password, user.hashed_password):
#         print(f"Invalid password for user: {form_data.username}")
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#
#     print(f"Login successful for user: {form_data.username}")
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @router.get("/users/me", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user
#
#
# @router.get("/test-auth")
# async def test_auth(current_user: User = Depends(get_current_active_user)):
#     return {
#         "message": "Authentication successful",
#         "user": current_user.username
#     }

# app/api/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from datetime import timedelta
import logging
from ...auth import (
    Token,
    User,
    create_access_token,
    get_user,
    verify_password,
    fake_users_db,
    get_current_active_user
)
from ...config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()
router = APIRouter()


@router.post("/token")
async def login_for_access_token(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends()
):
    logger.debug(f"Login attempt for user: {form_data.username}")

    try:
        user = get_user(fake_users_db, form_data.username)
        if not user:
            logger.warning(f"User not found: {form_data.username}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Incorrect username or password"
                },
                headers={"WWW-Authenticate": "Bearer"}
            )

        if not verify_password(form_data.password, user.hashed_password):
            logger.warning(f"Invalid password for user: {form_data.username}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Incorrect username or password"
                },
                headers={"WWW-Authenticate": "Bearer"}
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        logger.info(f"Login successful for user: {form_data.username}")
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error during authentication"}
        )


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/test")
async def test_auth(current_user: User = Depends(get_current_active_user)):
    """Test route to verify authentication is working"""
    return {
        "message": "Authentication successful",
        "user": current_user.username
    }