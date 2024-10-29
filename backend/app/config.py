from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path


class Settings(BaseSettings):
    # Base settings
    PROJECT_NAME: str = "Market Analysis API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./market_analysis.db"

    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ALPHA_VANTAGE_KEY: str = os.getenv("ALPHA_VANTAGE_KEY", "")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key")

    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]

    # Cache
    CACHE_DURATION: int = 300  # 5 minutes

    # Market Data
    DEFAULT_TIMEFRAME: str = "1d"
    DEFAULT_INTERVAL: str = "1m"

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


# Ensure SQLite database directory exists
db_path = Path("./market_analysis.db").parent
db_path.mkdir(parents=True, exist_ok=True)