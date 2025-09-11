from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

from ...models.database import get_db
from ...auth import get_current_active_user
from ...models.user import User
from ...services.ai_provider_service import ai_provider_service

router = APIRouter()
logger = logging.getLogger(__name__)


def _to_builtin(value):
    """Recursively convert numpy/pandas scalars to native Python types."""
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, (list, tuple)):
        return [_to_builtin(v) for v in value]
    if isinstance(value, dict):
        return {k: _to_builtin(v) for k, v in value.items()}
    return value

@router.get("/analysis/{symbol}")
async def get_market_analysis(
    symbol: str,
    timeframe: str = Query("1D", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$"),
    include_news: bool = Query(True),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive market analysis with AI insights using user's AI settings
    """
    try:
        # Get market data
        timeframe_map = {
            "1D": ("1d", "5m"),
            "1W": ("7d", "1h"),
            "1M": ("1mo", "1d"),
            "3M": ("3mo", "1d"),
            "6M": ("6mo", "1d"),
            "1Y": ("1y", "1d"),
            "YTD": ("ytd", "1d")
        }
        period, interval = timeframe_map.get(timeframe, ("1mo", "1h"))
        
        # Fetch market data
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
        
        if hist.empty:
            raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")
        
        # Get basic info
        info = ticker.info
        current_price = float(hist['Close'].iloc[-1])
        previous_price = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
        price_change = float(((current_price - previous_price) / previous_price) * 100) if previous_price else 0.0
        
        # Prepare market data for AI analysis
        market_data = {
            'symbol': symbol,
            'price': float(current_price),
            'change': float(current_price - previous_price),
            'change_percent': float(price_change),
            'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns and not pd.isna(hist['Volume'].iloc[-1]) else 0,
            'market_cap': int(info.get('marketCap') or 0),
            'pe_ratio': float(info.get('trailingPE') or 0),
            'chart_data': [float(x) for x in hist['Close'].tolist()[-7:]]  # Last 7 data points
        }
        
        # Calculate technical indicators
        technical_indicators = calculate_technical_indicators(hist)
        
        # Detect patterns
        patterns = detect_patterns(hist)
        
        # Generate signals
        signals = generate_signals(hist, technical_indicators)
        
        # Generate AI analysis using user's settings (structured for frontend)
        ai_analysis = None
        if current_user.ai_api_key:
            try:
                api_key = current_user.ai_api_key
                logger.info(f"User {current_user.username} - Provider: {current_user.ai_provider}, Model: {current_user.ai_model}")
                logger.info(f"API key starts with: {api_key[:20]}..." if api_key else "No API key")
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
                    logger.info(f"Generated structured AI analysis for {symbol} using {current_user.ai_provider}")
            except Exception as e:
                logger.error(f"AI analysis failed for {symbol}: {e}")
                ai_analysis = None
        
        response = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "market_data": {
                "current_price": current_price,
                "price_change": price_change,
                "volume": market_data['volume'],
                "market_cap": market_data['market_cap'],
                "pe_ratio": market_data['pe_ratio']
            },
            "technical_indicators": technical_indicators,
            "patterns": patterns,
            "signals": signals,
            "ai_analysis": ai_analysis,
            "timeframe": timeframe,
            "currency": "USD",
            "currencySymbol": "$"
        }
        return _to_builtin(response)
        
    except Exception as e:
        logger.error(f"Error in market analysis for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing market data: {str(e)}")

def calculate_technical_indicators(hist):
    """Calculate technical indicators and return under 'current' key."""
    if len(hist) < 2:
        return {"current": {}}

    close = hist['Close']
    current = {}

    # Moving Averages
    if len(hist) >= 20:
        sma_20 = close.rolling(window=20).mean().iloc[-1]
        current['sma_20'] = float(sma_20) if not pd.isna(sma_20) else None
    if len(hist) >= 50:
        sma_50 = close.rolling(window=50).mean().iloc[-1]
        current['sma_50'] = float(sma_50) if not pd.isna(sma_50) else None

    # RSI
    if len(hist) >= 14:
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        current['rsi'] = float(rsi) if not pd.isna(rsi) else None

    # MACD
    if len(hist) >= 26:
        exp12 = close.ewm(span=12, adjust=False).mean()
        exp26 = close.ewm(span=26, adjust=False).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9, adjust=False).mean()
        current['macd'] = float(macd.iloc[-1]) if not pd.isna(macd.iloc[-1]) else None
        current['macd_signal'] = float(signal.iloc[-1]) if not pd.isna(signal.iloc[-1]) else None

    # Bollinger Bands
    if len(hist) >= 20:
        sma = close.rolling(window=20).mean()
        std = close.rolling(window=20).std()
        if not pd.isna(sma.iloc[-1]) and not pd.isna(std.iloc[-1]):
            current['bb_upper'] = float(sma.iloc[-1] + (std.iloc[-1] * 2))
            current['bb_lower'] = float(sma.iloc[-1] - (std.iloc[-1] * 2))
            current['bb_middle'] = float(sma.iloc[-1])

    return {"current": current}

def detect_patterns(hist):
    """Detect simple patterns and normalize shape."""
    patterns = []
    if len(hist) < 10:
        return patterns

    recent = hist['Close'].tail(5)
    timestamp = datetime.now().isoformat()
    if recent.iloc[-1] > recent.iloc[0]:
        patterns.append({
            "type": "Uptrend",
            "confidence": 70,
            "description": "Price shows a short-term uptrend",
            "timestamp": timestamp
        })
    elif recent.iloc[-1] < recent.iloc[0]:
        patterns.append({
            "type": "Downtrend",
            "confidence": 70,
            "description": "Price shows a short-term downtrend",
            "timestamp": timestamp
        })

    return patterns

def generate_signals(hist, technical_indicators):
    """Generate signals including indicator and timeframe fields."""
    signals = []
    current = technical_indicators.get('current', {}) if isinstance(technical_indicators, dict) else {}
    if not current:
        return signals

    # RSI-based (short)
    rsi = current.get('rsi')
    if rsi is not None:
        if rsi < 30:
            signals.append({
                "type": "BUY",
                "strength": "STRONG",
                "indicator": "RSI",
                "reason": "Oversold condition (RSI < 30)",
                "timeframe": "short"
            })
        elif rsi > 70:
            signals.append({
                "type": "SELL",
                "strength": "STRONG",
                "indicator": "RSI",
                "reason": "Overbought condition (RSI > 70)",
                "timeframe": "short"
            })

    # MACD-based (medium)
    macd = current.get('macd')
    macd_signal = current.get('macd_signal')
    if macd is not None and macd_signal is not None:
        if macd > macd_signal:
            signals.append({
                "type": "BUY",
                "strength": "MEDIUM",
                "indicator": "MACD",
                "reason": f"Bullish crossover (MACD: {macd:.2f} > Signal: {macd_signal:.2f})",
                "timeframe": "medium"
            })
        elif macd < macd_signal:
            signals.append({
                "type": "SELL",
                "strength": "MEDIUM",
                "indicator": "MACD",
                "reason": f"Bearish crossover (MACD: {macd:.2f} < Signal: {macd_signal:.2f})",
                "timeframe": "medium"
            })

    # MA crossover (long)
    sma_20 = current.get('sma_20')
    sma_50 = current.get('sma_50')
    if sma_20 is not None and sma_50 is not None:
        if sma_20 > sma_50:
            signals.append({
                "type": "BUY",
                "strength": "MEDIUM",
                "indicator": "Moving Averages",
                "reason": "Golden Cross (SMA20 above SMA50)",
                "timeframe": "long"
            })
        elif sma_20 < sma_50:
            signals.append({
                "type": "SELL",
                "strength": "MEDIUM",
                "indicator": "Moving Averages",
                "reason": "Death Cross (SMA20 below SMA50)",
                "timeframe": "long"
            })

    return signals

@router.get("/indicators/{symbol}")
async def get_indicators(symbol: str, timeframe: str = Query("1M", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$")):
    timeframe_map = {
        "1D": ("1d", "5m"),
        "1W": ("7d", "1h"),
        "1M": ("1mo", "1d"),
        "3M": ("3mo", "1d"),
        "6M": ("6mo", "1d"),
        "1Y": ("1y", "1d"),
        "YTD": ("ytd", "1d")
    }
    period, interval = timeframe_map.get(timeframe, ("1mo", "1d"))
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval=interval)
    if hist.empty:
        raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")
    indicators = calculate_technical_indicators(hist)
    return _to_builtin({"technical_indicators": indicators})

@router.get("/patterns/{symbol}")
async def get_patterns(symbol: str, timeframe: str = Query("1M", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$")):
    timeframe_map = {
        "1D": ("1d", "5m"),
        "1W": ("7d", "1h"),
        "1M": ("1mo", "1d"),
        "3M": ("3mo", "1d"),
        "6M": ("6mo", "1d"),
        "1Y": ("1y", "1d"),
        "YTD": ("ytd", "1d")
    }
    period, interval = timeframe_map.get(timeframe, ("1mo", "1d"))
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval=interval)
    if hist.empty:
        raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")
    patterns = detect_patterns(hist)
    return _to_builtin({"patterns": patterns})

@router.get("/signals/{symbol}")
async def get_signals(symbol: str, timeframe: str = Query("1M", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$")):
    timeframe_map = {
        "1D": ("1d", "5m"),
        "1W": ("7d", "1h"),
        "1M": ("1mo", "1d"),
        "3M": ("3mo", "1d"),
        "6M": ("6mo", "1d"),
        "1Y": ("1y", "1d"),
        "YTD": ("ytd", "1d")
    }
    period, interval = timeframe_map.get(timeframe, ("1mo", "1d"))
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval=interval)
    if hist.empty:
        raise HTTPException(status_code=404, detail=f"Market data not found for symbol {symbol}")
    indicators = calculate_technical_indicators(hist)
    signals = generate_signals(hist, indicators)
    return _to_builtin({"signals": signals})
