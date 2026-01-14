"""
Market Analysis API Routes

Provides comprehensive market analysis with technical indicators,
pattern detection, signals, risk metrics, and AI insights.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import yfinance as yf
import pandas as pd
from datetime import datetime
import logging

from ...models.database import get_db
from ...auth import get_current_active_user
from ...models.user import User
from ...services.ai_provider_service import ai_provider_service
from ...services.api_token_service import APITokenService

# Import from new modular services
from ...services.technical_indicators import calculate_technical_indicators
from ...services.pattern_detection import detect_patterns
from ...services.signal_generation import generate_signals
from ...services.risk_metrics import calculate_risk_metrics
from ...api.utils.market_utils import (
    fetch_yfinance_data,
    get_market_data_info,
    _to_builtin,
    TIMEFRAME_MAP,
    get_timestamp
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/analysis/{symbol}")
async def get_market_analysis(
    symbol: str,
    timeframe: str = Query("1D", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$"),
    include_news: bool = Query(True),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive market analysis with AI insights using user's AI settings.
    """
    try:
        # Fetch market data using utility
        hist = fetch_yfinance_data(symbol, timeframe)

        if hist is None or hist.empty:
            raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")

        # Get ticker info
        ticker = yf.Ticker(symbol)

        # Prepare market data for AI analysis
        market_data = get_market_data_info(ticker, hist)

        # Calculate technical indicators using modular service
        technical_indicators = calculate_technical_indicators(hist)

        # Detect patterns using modular service
        try:
            patterns = detect_patterns(hist)
        except Exception as e:
            logger.error(f"Error detecting patterns for {symbol}: {str(e)}")
            patterns = []

        # Generate signals using modular service
        signals = generate_signals(hist, technical_indicators)

        # Calculate risk metrics using modular service
        risk_metrics = calculate_risk_metrics(hist, technical_indicators)

        # Generate AI analysis using user's settings (structured for frontend)
        ai_analysis = None
        if APITokenService.has_api_key(current_user):
            try:
                # Decrypt API key from token
                api_key = APITokenService.get_api_key(db, current_user)
                if api_key:
                    ai_analysis = await ai_provider_service.generate_structured_market_analysis(
                        symbol=symbol,
                        market_data=market_data,
                        technical_indicators=technical_indicators,
                        patterns=patterns,
                        provider=current_user.ai_provider,
                        model=current_user.ai_model,
                        api_key=api_key,
                        timeframe=timeframe,
                        temperature=float(current_user.ai_temperature),
                        max_tokens=current_user.ai_max_tokens
                    )
            except Exception as e:
                logger.error(f"AI analysis failed for {symbol}: {e}")
                ai_analysis = None

        response = {
            "symbol": symbol,
            "timestamp": get_timestamp(),
            "market_data": {
                "current_price": market_data['price'],
                "price_change": market_data['change_percent'],
                "volume": market_data['volume'],
                "market_cap": market_data['market_cap'],
                "pe_ratio": market_data['pe_ratio']
            },
            "technical_indicators": technical_indicators,
            "patterns": patterns,
            "signals": signals,
            "risk_metrics": risk_metrics,
            "ai_analysis": ai_analysis,
            "timeframe": timeframe,
            "currency": "USD",
            "currencySymbol": "$"
        }
        return _to_builtin(response)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in market analysis for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing market data: {str(e)}")


# Individual endpoint for technical indicators
@router.get("/indicators/{symbol}")
async def get_indicators(
    symbol: str,
    timeframe: str = Query("1M", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$"),
    current_user: User = Depends(get_current_active_user)
):
    """Get technical indicators for a symbol."""
    try:
        hist = fetch_yfinance_data(symbol, timeframe)
        if hist is None or hist.empty:
            raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")

        indicators = calculate_technical_indicators(hist)
        return _to_builtin(indicators)
    except Exception as e:
        logger.error(f"Error calculating indicators for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating indicators: {str(e)}")


# Individual endpoint for patterns
@router.get("/patterns/{symbol}")
async def get_patterns(
    symbol: str,
    timeframe: str = Query("1M", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$"),
    current_user: User = Depends(get_current_active_user)
):
    """Get detected patterns for a symbol."""
    try:
        hist = fetch_yfinance_data(symbol, timeframe)
        if hist is None or hist.empty:
            raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")

        patterns = detect_patterns(hist)
        return _to_builtin(patterns)
    except Exception as e:
        logger.error(f"Error detecting patterns for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error detecting patterns: {str(e)}")


# Individual endpoint for signals
@router.get("/signals/{symbol}")
async def get_signals(
    symbol: str,
    timeframe: str = Query("1M", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$"),
    current_user: User = Depends(get_current_active_user)
):
    """Get trading signals for a symbol."""
    try:
        hist = fetch_yfinance_data(symbol, timeframe)
        if hist is None or hist.empty:
            raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")

        indicators = calculate_technical_indicators(hist)
        signals = generate_signals(hist, indicators)
        return _to_builtin(signals)
    except Exception as e:
        logger.error(f"Error generating signals for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating signals: {str(e)}")


# Individual endpoint for risk metrics
@router.get("/risk-metrics/{symbol}")
async def get_risk_metrics_endpoint(
    symbol: str,
    timeframe: str = Query("1M", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$"),
    current_user: User = Depends(get_current_active_user)
):
    """Get risk metrics for a symbol."""
    try:
        hist = fetch_yfinance_data(symbol, timeframe)
        if hist is None or hist.empty:
            raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")

        indicators = calculate_technical_indicators(hist)
        risk_metrics = calculate_risk_metrics(hist, indicators)
        return _to_builtin(risk_metrics)
    except Exception as e:
        logger.error(f"Error calculating risk metrics for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating risk metrics: {str(e)}")
