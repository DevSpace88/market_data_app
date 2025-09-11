# models/user.py
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from passlib.context import CryptContext
from .database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # AI Provider Settings
    ai_provider = Column(String, default="openai")  # openai, deepseek, anthropic, etc.
    ai_api_key = Column(Text, nullable=True)  # Encrypted API key
    ai_model = Column(String, default="gpt-3.5-turbo")  # Model name
    ai_temperature = Column(String, default="0.7")  # Temperature setting
    ai_max_tokens = Column(Integer, default=1000)  # Max tokens
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    watchlists = relationship("Watchlist", back_populates="user")

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)