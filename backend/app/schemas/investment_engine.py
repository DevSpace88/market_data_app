"""
Pydantic Schemas for Investment Decision Engine

Request and response schemas for:
- Master Investment Score
- Sentiment Analysis
- Unusual Activity Detection
- Signal Performance Tracking
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============================================================================
# Master Investment Score Schemas
# ============================================================================

class ScoreBreakdown(BaseModel):
    """Individual score component breakdown"""
    score: float = Field(..., description="Score value (0-100)")
    weight: float = Field(..., description="Weight in final calculation")
    label: str = Field(..., description="Human-readable label")


class TopFactor(BaseModel):
    """Top contributing factor"""
    name: str = Field(..., description="Factor name")
    score: float = Field(..., description="Factor score")
    contribution: float = Field(..., description="Contribution to final score")


class MasterScoreResponse(BaseModel):
    """Response from master score calculation"""
    master_score: float = Field(..., ge=0, le=100, description="Overall score 0-100")
    recommendation: str = Field(..., description="STRONG_BUY, BUY, HOLD, SELL, or STRONG_SELL")
    confidence: str = Field(..., description="HIGH, MEDIUM, or LOW")
    breakdown: Dict[str, ScoreBreakdown] = Field(..., description="Component breakdown")
    top_factors: List[TopFactor] = Field(default_factory=list, description="Top 3 contributing factors")
    timestamp: str = Field(..., description="ISO timestamp")


# ============================================================================
# Sentiment Analysis Schemas
# ============================================================================

class SentimentBreakdown(BaseModel):
    """Sentiment breakdown by source"""
    score: float = Field(..., ge=-100, le=100, description="Sentiment score")
    count: int = Field(..., ge=0, description="Number of items analyzed")
    positive: int = Field(..., ge=0, description="Positive items count")
    negative: int = Field(..., ge=0, description="Negative items count")
    neutral: int = Field(..., ge=0, description="Neutral items count")


class TopHeadline(BaseModel):
    """Top news headline with sentiment"""
    title: str = Field(..., description="Headline title")
    sentiment_contribution: str = Field(..., description="Sentiment impact")
    timestamp: Optional[str] = Field(None, description="Publication timestamp")
    link: Optional[str] = Field(None, description="Article link")


class SocialBuzz(BaseModel):
    """Social media buzz metrics"""
    score: float = Field(default=0, ge=0, le=100, description="Buzz score 0-100")
    trend: str = Field(default="STABLE", description="RISING, STABLE, or FALLING")
    mentions_24h: int = Field(default=0, ge=0, description="Mentions in last 24h")


class SentimentAnalysisResponse(BaseModel):
    """Response from sentiment analysis"""
    symbol: str = Field(..., description="Stock symbol")
    sentiment_score: float = Field(..., ge=-100, le=100, description="Overall sentiment score")
    sentiment_label: str = Field(..., description="Human-readable sentiment label")
    confidence: str = Field(..., description="HIGH, MEDIUM, or LOW")
    breakdown: Dict[str, SentimentBreakdown] = Field(..., description="Sentiment by source")
    top_headlines: List[TopHeadline] = Field(default_factory=list, description="Top 3 headlines")
    social_buzz: SocialBuzz = Field(default_factory=SocialBuzz, description="Social media metrics")
    price_correlation: Optional[float] = Field(None, description="Correlation with price")
    data_sources: str = Field(..., description="Data sources used")
    timestamp: str = Field(..., description="ISO timestamp")
    warning: Optional[str] = Field(None, description="Warning message if applicable")
    error: Optional[str] = Field(None, description="Error message if applicable")


# ============================================================================
# Unusual Activity Schemas
# ============================================================================

class ActivityDetails(BaseModel):
    """Details of unusual activity"""
    current_volume: Optional[int] = Field(None, description="Current volume")
    average_volume: Optional[int] = Field(None, description="Average volume")
    ratio: Optional[float] = Field(None, description="Ratio to average")
    z_score: Optional[float] = Field(None, description="Z-score")
    deviation: Optional[str] = Field(None, description="Deviation description")
    current_price: Optional[float] = Field(None, description="Current price")
    average_price: Optional[float] = Field(None, description="Average price")
    daily_change_percent: Optional[float] = Field(None, description="Daily change %")


class UnusualActivity(BaseModel):
    """Detected unusual activity"""
    type: str = Field(..., description="Activity type: VOLUME_SPIKE, PRICE_ANOMALY, etc.")
    severity: str = Field(..., description="LOW, MEDIUM, HIGH, or EXTREME")
    confidence: int = Field(..., ge=0, le=100, description="Confidence 0-100")
    details: ActivityDetails = Field(..., description="Activity details")
    price_at_detection: Optional[float] = Field(None, description="Price at detection")
    timestamp: Optional[str] = Field(None, description="Detection timestamp")
    interpretation: Optional[str] = Field(None, description="Human-readable interpretation")


class UnusualActivityResponse(BaseModel):
    """Response from unusual activity detection"""
    symbol: str = Field(..., description="Stock symbol")
    has_unusual_activity: bool = Field(..., description="Whether unusual activity was detected")
    activities: List[UnusualActivity] = Field(default_factory=list, description="Detected activities")
    overall_severity: str = Field(..., description="Overall severity level")
    timestamp: str = Field(..., description="ISO timestamp")
    warning: Optional[str] = Field(None, description="Warning message if applicable")
    error: Optional[str] = Field(None, description="Error message if applicable")


# ============================================================================
# Signal Performance Schemas
# ============================================================================

class PerformanceByType(BaseModel):
    """Performance by signal type"""
    count: int = Field(..., ge=0, description="Number of signals")
    win_rate: float = Field(..., ge=0, le=100, description="Win rate percentage")
    avg_return: float = Field(..., description="Average return percent")


class OverallPerformance(BaseModel):
    """Overall performance metrics"""
    total_signals: int = Field(..., ge=0, description="Total signals evaluated")
    profitable_signals: int = Field(..., ge=0, description="Profitable signals count")
    win_rate: float = Field(..., ge=0, le=100, description="Overall win rate")
    avg_return_percent: float = Field(..., description="Average return")
    avg_benchmark_return_percent: float = Field(..., description="Average benchmark return")
    avg_excess_return_percent: float = Field(..., description="Average excess return")


class VsBenchmark(BaseModel):
    """Comparison with benchmark"""
    outperformed: int = Field(..., ge=0, description="Signals that outperformed")
    underperformed: int = Field(..., ge=0, description="Signals that underperformed")
    beat_rate: float = Field(..., ge=0, le=100, description="Percentage that beat benchmark")


class SignalPerformanceResponse(BaseModel):
    """Response from signal performance query"""
    overall: OverallPerformance = Field(..., description="Overall metrics")
    by_signal_type: Dict[str, PerformanceByType] = Field(default_factory=dict, description="By signal type")
    by_timeframe: Dict[str, PerformanceByType] = Field(default_factory=dict, description="By timeframe")
    vs_benchmark: VsBenchmark = Field(..., description="Benchmark comparison")
    timestamp: str = Field(..., description="ISO timestamp")
    message: Optional[str] = Field(None, description="Informational message")
    error: Optional[str] = Field(None, description="Error message if applicable")


# ============================================================================
# Combined Decision Engine Response
# ============================================================================

class InvestmentDecisionResponse(BaseModel):
    """Complete investment decision response"""
    symbol: str = Field(..., description="Stock symbol")

    # Master Score
    master_score: MasterScoreResponse = Field(..., description="Master investment score")

    # Sentiment
    sentiment: Optional[SentimentAnalysisResponse] = Field(None, description="Sentiment analysis")

    # Unusual Activity
    unusual_activity: Optional[UnusualActivityResponse] = Field(None, description="Unusual activity")

    # Performance
    signal_performance: Optional[SignalPerformanceResponse] = Field(None, description="Historical performance")

    # Meta
    generated_at: str = Field(..., description="ISO timestamp")
    data_quality: str = Field(..., description="Overall data quality")


# ============================================================================
# Request Schemas
# ============================================================================

class MasterScoreRequest(BaseModel):
    """Request for master score calculation"""
    symbol: str = Field(..., description="Stock symbol")
    include_sentiment: bool = Field(default=True, description="Include sentiment in score")
    include_activity: bool = Field(default=True, description="Include unusual activity in score")


class SentimentAnalysisRequest(BaseModel):
    """Request for sentiment analysis"""
    symbol: str = Field(..., description="Stock symbol")
    use_ai: bool = Field(default=False, description="Use AI for deeper analysis")


class UnusualActivityRequest(BaseModel):
    """Request for unusual activity detection"""
    symbol: str = Field(..., description="Stock symbol")


class SignalPerformanceRequest(BaseModel):
    """Request for signal performance metrics"""
    symbol: Optional[str] = Field(None, description="Filter by symbol")
    signal_type: Optional[str] = Field(None, description="Filter by signal type")
    timeframe_days: Optional[int] = Field(None, description="Filter by timeframe")
