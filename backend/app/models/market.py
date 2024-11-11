# from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from .database import Base
#
#
# class Stock(Base):
#     __tablename__ = "stocks"
#
#     id = Column(Integer, primary_key=True, index=True)
#     symbol = Column(String, unique=True, index=True)
#     name = Column(String)
#     exchange = Column(String)
#     sector = Column(String)
#     industry = Column(String)
#     market_data = relationship("MarketData", back_populates="stock")
#     analysis_reports = relationship("AnalysisReport", back_populates="stock")
#
#
# class MarketData(Base):
#     __tablename__ = "market_data"
#
#     id = Column(Integer, primary_key=True, index=True)
#     stock_id = Column(Integer, ForeignKey("stocks.id"))
#     timestamp = Column(DateTime, default=datetime.utcnow)
#     data = Column(JSON)  # Speichert die YFinance Daten
#     cache_until = Column(DateTime)
#
#     stock = relationship("Stock", back_populates="market_data")
#
#
# class AnalysisReport(Base):
#     __tablename__ = "analysis_reports"
#
#     id = Column(Integer, primary_key=True, index=True)
#     stock_id = Column(Integer, ForeignKey("stocks.id"))
#     timestamp = Column(DateTime, default=datetime.utcnow)
#     report_type = Column(String)  # z.B. "technical", "ai", etc.
#     data = Column(JSON)
#     cache_until = Column(DateTime)
#
#     stock = relationship("Stock", back_populates="analysis_reports")



# models/market.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


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