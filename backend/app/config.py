# # # backend/app/config.py
# # from pydantic_settings import BaseSettings
# # from functools import lru_cache
# # from typing import List
# #
# # class Settings(BaseSettings):
# #     # Database Configuration
# #     DATABASE_URL: str = "sqlite:///./market_analysis.db"
# #
# #     # API Keys
# #     OPENAI_API_KEY: str
# #     ALPHA_VANTAGE_KEY: str | None = None  # Optional
# #
# #     # Security
# #     SECRET_KEY: str
# #     JWT_SECRET_KEY: str | None = None  # Optional
# #
# #     # API Configuration
# #     API_PREFIX: str = "/api/v1"
# #     PROJECT_NAME: str = "Market Analysis API"
# #     VERSION: str = "1.0.0"
# #
# #     # CORS Settings
# #     BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
# #
# #     # Cache Settings
# #     CACHE_DURATION: int = 300
# #
# #     # Market Data Settings
# #     DEFAULT_TIMEFRAME: str = "1d"
# #     DEFAULT_INTERVAL: str = "1m"
# #
# #     @property
# #     def cors_origins(self) -> List[str]:
# #         return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]
# #
# #     class Config:
# #         env_file = ".env"
# #         case_sensitive = True
# #         # Allow env variables not defined in the model
# #         extra = "ignore"
# #
# # @lru_cache()
# # def get_settings():
# #     return Settings()
#
#
# # backend/app/config.py
# from pydantic_settings import BaseSettings
# from functools import lru_cache
# from typing import List
# import secrets
#
# class Settings(BaseSettings):
#     # Database Configuration
#     DATABASE_URL: str = "sqlite:///./market_analysis.db"
#
#     # API Keys
#     OPENAI_API_KEY: str
#     ALPHA_VANTAGE_KEY: str | None = None  # Optional
#
#     # Security
#     SECRET_KEY: str
#     JWT_SECRET_KEY: str | None = None  # Optional
#
#     # Auth Settings
#     AUTH_ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
#     REFRESH_TOKEN_EXPIRE_DAYS: int = 7
#     MIN_PASSWORD_LENGTH: int = 8
#
#     # API Configuration
#     API_PREFIX: str = "/api/v1"
#     PROJECT_NAME: str = "Market Analysis API"
#     VERSION: str = "1.0.0"
#
#     # CORS Settings
#     BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
#
#     # Cache Settings
#     CACHE_DURATION: int = 300
#
#     # Market Data Settings
#     DEFAULT_TIMEFRAME: str = "1d"
#     DEFAULT_INTERVAL: str = "1m"
#
#     # Debug Settings
#     DEBUG: bool = False
#
#     @property
#     def cors_origins(self) -> List[str]:
#         return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]
#
#     @property
#     def auth_secret_key(self) -> str:
#         """Use JWT_SECRET_KEY if set, otherwise fall back to SECRET_KEY"""
#         return self.JWT_SECRET_KEY or self.SECRET_KEY
#
#     def generate_secret_key(self) -> str:
#         """Generate a secure secret key"""
#         return secrets.token_urlsafe(32)
#
#     class Config:
#         env_file = ".env"
#         case_sensitive = True
#         # Allow env variables not defined in the model
#         extra = "ignore"
#
# @lru_cache()
# def get_settings():
#     return Settings()
#
# # Usage example in other files:
# # from .config import get_settings
# # settings = get_settings()


# backend/app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./market_analysis.db"

    # API Keys
    OPENAI_API_KEY: str
    ALPHA_VANTAGE_KEY: str | None = None  # Optional

    # Security & Auth Settings
    SECRET_KEY: str
    JWT_SECRET_KEY: str | None = None  # Optional
    ALGORITHM: str = "HS256"  # Neu
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Neu

    # API Configuration
    API_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Market Analysis API"
    VERSION: str = "1.0.0"

    # CORS Settings
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Cache Settings
    CACHE_DURATION: int = 300

    # Market Data Settings
    DEFAULT_TIMEFRAME: str = "1d"
    DEFAULT_INTERVAL: str = "1m"

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]

    @property
    def auth_secret_key(self) -> str:
        """Use JWT_SECRET_KEY if set, otherwise fall back to SECRET_KEY"""
        return self.JWT_SECRET_KEY or self.SECRET_KEY

    class Config:
        env_file = ".env"
        case_sensitive = True
        # Allow env variables not defined in the model
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()