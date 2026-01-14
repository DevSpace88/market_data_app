"""
Investment Decision Engine Models

Stores sentiment analysis, unusual activity, and signal performance data.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class SentimentAnalysis(Base):
    """AI-powered sentiment analysis from news and social media"""
    __tablename__ = "sentiment_analysis"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Overall sentiment score (-100 to +100)
    sentiment_score = Column(Float, nullable=False)
    sentiment_label = Column(String)  # "Extremely Bearish", "Bearish", "Neutral", "Bullish", "Extremely Bullish"
    confidence = Column(String)  # "HIGH", "MEDIUM", "LOW"

    # News sentiment
    news_sentiment = Column(Float)
    news_count = Column(Integer)

    # Social media sentiment
    social_sentiment = Column(Float)
    social_buzz_score = Column(Float)  # 0-100, volume of mentions
    social_trend = Column(String)  # "RISING", "STABLE", "FALLING"

    # Top news
    top_headlines = Column(Text)  # JSON array of top 3 headlines with sentiment contribution

    # Correlation with price
    price_sentiment_correlation = Column(Float)  # Correlation coefficient

    # Metadata
    data_sources = Column(String)  # Comma-separated list of sources
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Index for symbol + timestamp queries
    __table_args__ = (
        Index('ix_sentiment_symbol_timestamp', 'symbol', 'timestamp'),
    )


class UnusualActivity(Base):
    """Detected unusual market activity indicating institutional moves"""
    __tablename__ = "unusual_activity"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Activity type
    activity_type = Column(String, nullable=False)  # "VOLUME_SPIKE", "OPTIONS_FLOW", "DARK_POOL", "PRICE_ANOMALY"

    # Severity and confidence
    severity = Column(String)  # "LOW", "MEDIUM", "HIGH", "EXTREME"
    confidence = Column(Float)  # 0-100

    # Details (JSON string for flexibility)
    details = Column(Text)  # JSON: {"current_volume": 1000000, "avg_volume": 500000, "ratio": 2.0}

    # Context
    price_at_detection = Column(Float)
    volume_at_detection = Column(Float)
    benchmark_deviation = Column(Float)  # How many std devs from mean

    # Time since last activity
    hours_since_last_activity = Column(Integer)

    # Metadata
    is_active = Column(Boolean, default=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Index for active alerts
    __table_args__ = (
        Index('ix_unusual_activity_symbol_active', 'symbol', 'is_active'),
    )


class SignalPerformance(Base):
    """Historical performance tracking of generated signals"""
    __tablename__ = "signal_performance"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)

    # Signal details
    signal_type = Column(String, nullable=False)  # "BUY", "SELL", "HOLD"
    signal_strength = Column(String)  # "WEAK", "MEDIUM", "STRONG", "VERY_STRONG"
    master_score = Column(Float)  # 0-100

    # Timestamps
    generated_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    evaluated_at = Column(DateTime(timezone=True), nullable=True)

    # Performance metrics
    timeframe_days = Column(Integer)  # 1, 7, 30, etc.
    return_percent = Column(Float)  # Actual return
    benchmark_return_percent = Column(Float)  # S&P 500 return in same period
    excess_return = Column(Float)  # return_percent - benchmark_return_percent

    # Outcome
    is_profitable = Column(Boolean)
    is_pending = Column(Boolean, default=True)  # True if not yet evaluated

    # Components that contributed
    technical_score = Column(Float)
    sentiment_score = Column(Float)
    activity_score = Column(Float)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Index for performance queries
    __table_args__ = (
        Index('ix_signal_performance_symbol_timeframe', 'symbol', 'timeframe_days', 'evaluated_at'),
        Index('ix_signal_performance_pending', 'symbol', 'is_pending'),
    )
