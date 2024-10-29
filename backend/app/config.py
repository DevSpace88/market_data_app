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

    # Security
    SECRET_KEY: str
    JWT_SECRET_KEY: str | None = None  # Optional

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

    class Config:
        env_file = ".env"
        case_sensitive = True
        # Allow env variables not defined in the model
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()