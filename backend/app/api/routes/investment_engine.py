"""
Investment Decision Engine API Routes

Provides endpoints for:
- Master Investment Score calculation
- Sentiment Analysis
- Unusual Activity Detection
- Signal Performance Tracking
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import logging

from ...models.database import get_db
from ...auth import get_current_active_user, User
from ...api.utils.market_utils import (
    fetch_yfinance_data,
    get_market_data_info,
    _to_builtin,
    TIMEFRAME_MAP,
    get_timestamp
)

# Import functions from existing services (not classes!)
from ...services.technical_indicators import calculate_technical_indicators
from ...services.pattern_detection import detect_patterns
from ...services.signal_generation import generate_signals
from ...services.risk_metrics import calculate_risk_metrics
from ...services.master_score_service import MasterScoreService
from ...services.sentiment_service import SentimentAnalysisService
from ...services.unusual_activity_service import UnusualActivityService
from ...services.signal_performance_service import SignalPerformanceService

from ...schemas.investment_engine import (
    MasterScoreResponse,
    SentimentAnalysisResponse,
    UnusualActivityResponse,
    SignalPerformanceResponse,
    InvestmentDecisionResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/investment-engine", tags=["Investment Decision Engine"])


# ============================================================================
# Fetch Article Content (Proxy to avoid CORS)
# ============================================================================

@router.post("/fetch-article")
async def fetch_article_content(
    request: dict,
    current_user: User = Depends(get_current_active_user)
):
    """
    Fetch article content from URL (proxy to avoid CORS).
    Used by the news article dialog to display full article content.
    """
    try:
        url = request.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="URL is required")

        # Fetch article content
        import requests
        from bs4 import BeautifulSoup

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Try to find the article content
        # Yahoo Finance specific selectors
        article_content = None

        # Method 1: Try Yahoo Finance specific div
        article_div = soup.find('div', class_='caas-body')
        if article_div:
            article_content = article_div.get_text(strip=True)
        else:
            # Method 2: Try main content area
            article_div = soup.find('article')
            if article_div:
                article_content = article_div.get_text(strip=True)
            else:
                # Method 3: Try to find any div with substantial text
                for div in soup.find_all('div'):
                    text = div.get_text(strip=True)
                    if len(text) > 500:  # Only if substantial content
                        article_content = text
                        break

        if article_content:
            # Clean up the content
            article_content = ' '.join(article_content.split())
            return {
                "content": article_content[:5000],  # Limit to 5000 chars
                "url": url
            }
        else:
            return {
                "content": "Could not extract article content. Please open the original article.",
                "url": url
            }

    except requests.Timeout:
        raise HTTPException(status_code=408, detail="Request timeout")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch article: {str(e)}")
    except Exception as e:
        logger.error(f"Error fetching article: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing article: {str(e)}")


# Helper function to convert hist to market data list
def _hist_to_market_data_list(hist):
    """Convert pandas DataFrame to market data list format"""
    import pandas as pd
    market_data = []
    for idx, row in hist.iterrows():
        market_data.append({
            'timestamp': idx.isoformat(),
            'open': float(row['Open']),
            'high': float(row['High']),
            'low': float(row['Low']),
            'close': float(row['Close']),
            'volume': int(row['Volume']) if 'Volume' in row and pd.notna(row['Volume']) else 0
        })
    return market_data


# ============================================================================
# Master Investment Score Endpoints
# ============================================================================

@router.get("/master-score/{symbol}", response_model=MasterScoreResponse)
async def get_master_score(
    symbol: str,
    timeframe: str = Query("1Y", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Calculate the Master Investment Score (0-100) for a symbol.

    The score combines:
    - Short-term signals (30%): RSI, Stochastic, Williams %R
    - Medium-term signals (30%): MACD, ADX, SMA crossovers
    - Long-term signals (20%): Trends, Support/Resistance
    - Risk metrics (20%): Volatility, Drawdown

    Returns a score with recommendation (STRONG_BUY to STRONG_SELL).
    """
    try:
        # Fetch market data using existing utility
        hist = fetch_yfinance_data(symbol, timeframe)

        if hist is None or hist.empty:
            raise HTTPException(status_code=404, detail=f"Market data not found for {symbol}")

        # Calculate technical indicators (using existing function)
        technical_indicators = calculate_technical_indicators(hist)

        # Generate signals (using existing function)
        signals = generate_signals(hist, technical_indicators)

        # Calculate risk metrics (using existing function)
        risk_metrics = calculate_risk_metrics(hist, technical_indicators)

        # Detect patterns
        patterns = detect_patterns(hist)

        # Calculate master score
        score_service = MasterScoreService()
        result = score_service.calculate_master_score(
            technical_indicators=technical_indicators,
            signals=signals,
            risk_metrics=risk_metrics,
            patterns=patterns
        )

        return _to_builtin(result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating master score for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Error calculating master score: {str(e)}")


# ============================================================================
# Sentiment Analysis Endpoints
# ============================================================================

@router.get("/sentiment/{symbol}", response_model=SentimentAnalysisResponse)
async def get_sentiment_analysis(
    symbol: str,
    use_ai: bool = Query(False, description="Use AI for deeper analysis"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Analyze sentiment from news and social media for a symbol.

    Returns sentiment score (-100 to +100) with:
    - News sentiment breakdown
    - Top headlines with sentiment contribution
    - Social media buzz metrics
    - AI-powered insights (if use_ai=True)
    """
    try:
        sentiment_service = SentimentAnalysisService(db)
        result = await sentiment_service.analyze_sentiment(symbol, use_ai=use_ai)
        return _to_builtin(result)

    except Exception as e:
        logger.error(f"Error analyzing sentiment for {symbol}: {e}")
        # Return empty response instead of error - sentiment is optional
        return {
            "symbol": symbol,
            "sentiment_score": 0,
            "sentiment_label": "No Data",
            "confidence": "LOW",
            "breakdown": {"news": {"score": 0, "count": 0, "positive": 0, "negative": 0, "neutral": 0}},
            "top_headlines": [],
            "social_buzz": {"score": 0, "trend": "STABLE", "mentions_24h": 0},
            "price_correlation": None,
            "data_sources": "None",
            "timestamp": get_timestamp(),
            "warning": "Sentiment analysis unavailable"
        }


# ============================================================================
# Unusual Activity Endpoints
# ============================================================================

@router.get("/unusual-activity/{symbol}", response_model=UnusualActivityResponse)
async def get_unusual_activity(
    symbol: str,
    timeframe: str = Query("3mo", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Detect unusual market activity for a symbol.

    Detects:
    - Volume spikes (>3x standard deviation)
    - Price anomalies (>2.5x standard deviation)
    - Options flow activity (Phase 2)
    - Dark pool activity (Phase 2)

    Returns detected activities with severity and interpretation.
    """
    try:
        # Fetch market data
        hist = fetch_yfinance_data(symbol, timeframe)

        if hist is None or hist.empty:
            raise HTTPException(status_code=404, detail=f"Market data not found for {symbol}")

        # Convert to list format for unusual activity service
        market_data = _hist_to_market_data_list(hist)
        current_price = float(hist['Close'].iloc[-1]) if len(hist) > 0 else None

        # Detect unusual activity
        activity_service = UnusualActivityService(db)
        result = await activity_service.detect_unusual_activity(symbol, market_data, current_price)
        return _to_builtin(result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error detecting unusual activity for {symbol}: {e}")
        # Return empty response instead of error - activity is optional
        return {
            "symbol": symbol,
            "has_unusual_activity": False,
            "activities": [],
            "overall_severity": "ERROR",
            "timestamp": get_timestamp(),
            "error": "Unusual activity detection temporarily unavailable"
        }


# ============================================================================
# Signal Performance Endpoints
# ============================================================================

@router.get("/signal-performance")
async def get_signal_performance(
    symbol: Optional[str] = Query(None, description="Filter by symbol"),
    signal_type: Optional[str] = Query(None, description="Filter by signal type (BUY, SELL, HOLD)"),
    timeframe_days: Optional[int] = Query(None, description="Filter by timeframe (1, 7, 30)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get signal performance metrics.

    Returns:
    - Overall win rate and average returns
    - Performance by signal type
    - Performance by timeframe
    - Comparison with benchmark (S&P 500)
    """
    try:
        performance_service = SignalPerformanceService(db)
        result = performance_service.get_accuracy_metrics(
            symbol=symbol,
            signal_type=signal_type,
            timeframe_days=timeframe_days
        )
        return _to_builtin(result)

    except Exception as e:
        logger.error(f"Error getting signal performance: {e}")
        # Return empty response instead of error
        return {
            "overall": {
                "total_signals": 0,
                "profitable_signals": 0,
                "win_rate": 0,
                "avg_return_percent": 0,
                "avg_benchmark_return_percent": 0,
                "avg_excess_return_percent": 0
            },
            "by_signal_type": {},
            "by_timeframe": {},
            "vs_benchmark": {
                "outperformed": 0,
                "underperformed": 0,
                "beat_rate": 0
            },
            "timestamp": get_timestamp(),
            "message": "No performance data available yet"
        }


# ============================================================================
# Combined Decision Engine Endpoint
# ============================================================================

@router.get("/decision/{symbol}")
async def get_investment_decision(
    symbol: str,
    timeframe: str = Query("1Y", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$"),
    include_sentiment: bool = Query(True, description="Include sentiment analysis"),
    include_activity: bool = Query(True, description="Include unusual activity detection"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get complete investment decision analysis.

    This is the main endpoint that combines all analyses:
    - Master Investment Score (0-100)
    - Sentiment Analysis
    - Unusual Activity Detection
    - Signal Performance History

    Use this to get a comprehensive view before making investment decisions.
    """
    try:
        # Fetch market data using existing utility
        hist = fetch_yfinance_data(symbol, timeframe)

        if hist is None or hist.empty:
            raise HTTPException(status_code=404, detail=f"Market data not found for {symbol}")

        current_price = float(hist['Close'].iloc[-1]) if len(hist) > 0 else None

        # Calculate technical indicators (using existing function)
        technical_indicators = calculate_technical_indicators(hist)

        # Generate signals (using existing function)
        signals = generate_signals(hist, technical_indicators)

        # Calculate risk metrics (using existing function)
        risk_metrics = calculate_risk_metrics(hist, technical_indicators)

        # Detect patterns
        patterns = detect_patterns(hist)

        # Calculate master score
        score_service = MasterScoreService()
        master_score = score_service.calculate_master_score(
            technical_indicators=technical_indicators,
            signals=signals,
            risk_metrics=risk_metrics,
            patterns=patterns
        )

        # Sentiment analysis (optional)
        sentiment = None
        if include_sentiment:
            try:
                sentiment_service = SentimentAnalysisService(db)
                sentiment = await sentiment_service.analyze_sentiment(symbol, use_ai=False)
            except Exception as e:
                logger.warning(f"Sentiment analysis failed for {symbol}: {e}")

        # Unusual activity (optional)
        unusual_activity = None
        if include_activity:
            try:
                market_data = _hist_to_market_data_list(hist)
                activity_service = UnusualActivityService(db)
                unusual_activity = await activity_service.detect_unusual_activity(symbol, market_data, current_price)
            except Exception as e:
                logger.warning(f"Unusual activity detection failed for {symbol}: {e}")

        # Signal performance
        performance_service = SignalPerformanceService(db)
        signal_performance = performance_service.get_accuracy_metrics(symbol=symbol)

        # Calculate overall data quality
        available_indicators = sum(1 for v in technical_indicators.get('current', {}).values() if v is not None)
        total_indicators = len(technical_indicators.get('current', {}))
        data_quality = "HIGH" if (total_indicators > 0 and available_indicators / total_indicators >= 0.8) else "MEDIUM"

        response = {
            "symbol": symbol,
            "master_score": master_score,
            "sentiment": sentiment,
            "unusual_activity": unusual_activity,
            "signal_performance": signal_performance,
            "generated_at": master_score.get("timestamp", get_timestamp()),
            "data_quality": data_quality
        }

        return _to_builtin(response)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating investment decision for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating investment decision: {str(e)}")
