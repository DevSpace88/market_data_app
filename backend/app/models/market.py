from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    exchange = Column(String)
    sector = Column(String)
    industry = Column(String)
    market_data = relationship("MarketData", back_populates="stock")
    analysis_reports = relationship("AnalysisReport", back_populates="stock")


class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    data = Column(JSON)  # Speichert die YFinance Daten
    cache_until = Column(DateTime)

    stock = relationship("Stock", back_populates="market_data")


class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    report_type = Column(String)  # z.B. "technical", "ai", etc.
    data = Column(JSON)
    cache_until = Column(DateTime)

    stock = relationship("Stock", back_populates="analysis_reports")