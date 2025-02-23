# backend/app/config.py
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

# Get the directory containing config.py
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file using the correct path
load_dotenv(BASE_DIR / '.env')

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./market_analysis.db"

    # API Keys
    OPENAI_API_KEY: str = "sk-dummy-key"  # Standardwert hinzugefügt
    ALPHA_VANTAGE_KEY: str | None = None  # Optional

    # Security & Auth Settings
    SECRET_KEY: str = "default-secret-key"  # Standardwert hinzugefügt
    JWT_SECRET_KEY: str | None = None  # Optional
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

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
        env_file_encoding = 'utf-8'
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()