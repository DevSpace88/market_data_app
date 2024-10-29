from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from ..config import get_settings

settings = get_settings()

# SQLite setup
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Float)

    indicators = relationship("TechnicalIndicator", back_populates="market_data")


class TechnicalIndicator(Base):
    __tablename__ = "technical_indicators"

    id = Column(Integer, primary_key=True, index=True)
    market_data_id = Column(Integer, ForeignKey("market_data.id"))
    indicator_type = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    market_data = relationship("MarketData", back_populates="indicators")


class SentimentData(Base):
    __tablename__ = "sentiment_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    source = Column(String)
    sentiment_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    text = Column(String)


class PatternDetection(Base):
    __tablename__ = "pattern_detections"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    pattern_type = Column(String)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    description = Column(String)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create all tables
Base.metadata.create_all(bind=engine)