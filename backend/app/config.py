# backend/app/config.py
import os
import secrets
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from typing import List, Optional

# Get the directory containing config.py
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file using the correct path
load_dotenv(BASE_DIR / '.env')

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./market_analysis.db"

    # Railway PostgreSQL Configuration
    RAILWAY_DATABASE_URL: Optional[str] = None

    # API Keys
    OPENAI_API_KEY: str = "sk-dummy-key"  # Standardwert hinzugefügt (deprecated)
    ALPHA_VANTAGE_KEY: Optional[str] = None  # Optional

    # Security & Auth Settings
    # SECRET_KEY can be provided via:
    # 1. SECRET_KEY env variable
    # 2. SECRET_KEY_FILE env variable (path to file containing key)
    # 3. Auto-generated and stored in .secret_key file (development only)
    SECRET_KEY: str = Field(default="default-secret-key", description="JWT signing key")
    SECRET_KEY_FILE: Optional[str] = Field(default=None, description="Path to file containing SECRET_KEY")
    JWT_SECRET_KEY: Optional[str] = Field(default=None, description="Optional separate JWT secret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API Configuration
    API_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Market Analysis API"
    VERSION: str = "1.0.0"

    # CORS Settings
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:5174,http://localhost:3000"

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
        """
        Get the actual secret key for JWT signing.

        Priority order:
        1. JWT_SECRET_KEY if set
        2. SECRET_KEY from env variable
        3. SECRET_KEY from file specified by SECRET_KEY_FILE
        4. Auto-generated key from .secret_key file (development)
        """
        if self.JWT_SECRET_KEY:
            return self.JWT_SECRET_KEY

        # Check SECRET_KEY_FILE first
        if self.SECRET_KEY_FILE:
            key_path = Path(self.SECRET_KEY_FILE)
            if key_path.exists():
                return key_path.read_text().strip()

        # Check .secret_key file in project root
        secret_key_path = BASE_DIR / ".secret_key"
        if secret_key_path.exists():
            return secret_key_path.read_text().strip()

        # Return default (will be validated on startup)
        return self.SECRET_KEY

    @property
    def database_url(self) -> str:
        """Use Railway PostgreSQL if available, otherwise fall back to SQLite"""
        return self.RAILWAY_DATABASE_URL or self.DATABASE_URL

    def is_using_default_secret_key(self) -> bool:
        """Check if using the insecure default secret key."""
        actual_key = self.auth_secret_key
        return actual_key in ("default-secret-key", "")

    def generate_secret_key(self) -> str:
        """Generate a cryptographically secure secret key."""
        return secrets.token_urlsafe(32)

    def ensure_secret_key(self) -> str:
        """
        Ensure a secure secret key exists.
        Generates and stores one if using default.
        """
        if self.is_using_default_secret_key():
            new_key = self.generate_secret_key()
            secret_key_path = BASE_DIR / ".secret_key"
            secret_key_path.write_text(new_key)
            os.chmod(secret_key_path, 0o600)
            return new_key
        return self.auth_secret_key

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()