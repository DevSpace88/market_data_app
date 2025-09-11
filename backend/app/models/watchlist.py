# models/watchlist.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Watchlist(Base):
    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String, nullable=False)
    display_name = Column(String, nullable=True)  # Optional: Custom name for the symbol
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to User
    user = relationship("User", back_populates="watchlists")

    def __repr__(self):
        return f"<Watchlist(id={self.id}, user_id={self.user_id}, symbol='{self.symbol}')>"
