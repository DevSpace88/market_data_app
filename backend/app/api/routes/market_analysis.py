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
        
        # Calculate risk metrics
        risk_metrics = calculate_risk_metrics(hist, technical_indicators)
        
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
            "risk_metrics": risk_metrics,
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
    """Calculate comprehensive technical indicators for quantitative trading."""
    if len(hist) < 2:
        return {"current": {}}

    close = hist['Close']
    high = hist['High']
    low = hist['Low']
    volume = hist['Volume'] if 'Volume' in hist.columns else None
    current = {}

    # === MOVING AVERAGES ===
    if len(hist) >= 20:
        sma_20 = close.rolling(window=20).mean().iloc[-1]
        current['sma_20'] = float(sma_20) if not pd.isna(sma_20) else None
    if len(hist) >= 50:
        sma_50 = close.rolling(window=50).mean().iloc[-1]
        current['sma_50'] = float(sma_50) if not pd.isna(sma_50) else None
    if len(hist) >= 200:
        sma_200 = close.rolling(window=200).mean().iloc[-1]
        current['sma_200'] = float(sma_200) if not pd.isna(sma_200) else None

    # EMA
    if len(hist) >= 12:
        ema_12 = close.ewm(span=12, adjust=False).mean().iloc[-1]
        current['ema_12'] = float(ema_12) if not pd.isna(ema_12) else None
    if len(hist) >= 26:
        ema_26 = close.ewm(span=26, adjust=False).mean().iloc[-1]
        current['ema_26'] = float(ema_26) if not pd.isna(ema_26) else None

    # === MOMENTUM INDICATORS ===
    # RSI
    if len(hist) >= 14:
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        current['rsi'] = float(rsi) if not pd.isna(rsi) else None

    # Stochastic Oscillator
    if len(hist) >= 14:
        lowest_low = low.rolling(window=14).min()
        highest_high = high.rolling(window=14).max()
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=3).mean()
        current['stoch_k'] = float(k_percent.iloc[-1]) if not pd.isna(k_percent.iloc[-1]) else None
        current['stoch_d'] = float(d_percent.iloc[-1]) if not pd.isna(d_percent.iloc[-1]) else None

    # Williams %R
    if len(hist) >= 14:
        highest_high = high.rolling(window=14).max()
        lowest_low = low.rolling(window=14).min()
        williams_r = -100 * ((highest_high - close) / (highest_high - lowest_low))
        current['williams_r'] = float(williams_r.iloc[-1]) if not pd.isna(williams_r.iloc[-1]) else None

    # CCI (Commodity Channel Index)
    if len(hist) >= 20:
        typical_price = (high + low + close) / 3
        sma_tp = typical_price.rolling(window=20).mean()
        mad = typical_price.rolling(window=20).apply(lambda x: np.mean(np.abs(x - x.mean())))
        cci = (typical_price - sma_tp) / (0.015 * mad)
        current['cci'] = float(cci.iloc[-1]) if not pd.isna(cci.iloc[-1]) else None

    # === TREND INDICATORS ===
    # MACD
    if len(hist) >= 26:
        exp12 = close.ewm(span=12, adjust=False).mean()
        exp26 = close.ewm(span=26, adjust=False).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal
        current['macd'] = float(macd.iloc[-1]) if not pd.isna(macd.iloc[-1]) else None
        current['macd_signal'] = float(signal.iloc[-1]) if not pd.isna(signal.iloc[-1]) else None
        current['macd_histogram'] = float(histogram.iloc[-1]) if not pd.isna(histogram.iloc[-1]) else None

    # ADX (Average Directional Index)
    if len(hist) >= 14:
        high_diff = high.diff()
        low_diff = low.diff()
        plus_dm = high_diff.where((high_diff > low_diff) & (high_diff > 0), 0)
        minus_dm = -low_diff.where((low_diff > high_diff) & (low_diff > 0), 0)
        
        atr = calculate_atr(high, low, close, 14)
        plus_di = 100 * (plus_dm.rolling(window=14).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(window=14).mean() / atr)
        
        dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window=14).mean()
        
        current['adx'] = float(adx.iloc[-1]) if not pd.isna(adx.iloc[-1]) else None
        current['plus_di'] = float(plus_di.iloc[-1]) if not pd.isna(plus_di.iloc[-1]) else None
        current['minus_di'] = float(minus_di.iloc[-1]) if not pd.isna(minus_di.iloc[-1]) else None

    # === VOLATILITY INDICATORS ===
    # Bollinger Bands
    if len(hist) >= 20:
        sma = close.rolling(window=20).mean()
        std = close.rolling(window=20).std()
        if not pd.isna(sma.iloc[-1]) and not pd.isna(std.iloc[-1]):
            bb_upper = sma.iloc[-1] + (std.iloc[-1] * 2)
            bb_lower = sma.iloc[-1] - (std.iloc[-1] * 2)
            bb_middle = sma.iloc[-1]
            bb_width = (bb_upper - bb_lower) / bb_middle
            bb_percent = (close.iloc[-1] - bb_lower) / (bb_upper - bb_lower)
            
            current['bb_upper'] = float(bb_upper)
            current['bb_lower'] = float(bb_lower)
            current['bb_middle'] = float(bb_middle)
            current['bb_width'] = float(bb_width)
            current['bb_percent'] = float(bb_percent)

    # ATR (Average True Range)
    if len(hist) >= 14:
        atr = calculate_atr(high, low, close, 14)
        current['atr'] = float(atr.iloc[-1]) if not pd.isna(atr.iloc[-1]) else None

    # === VOLUME INDICATORS ===
    if volume is not None and len(hist) >= 20:
        # OBV (On-Balance Volume)
        obv = calculate_obv(close, volume)
        current['obv'] = float(obv.iloc[-1]) if not pd.isna(obv.iloc[-1]) else None
        
        # Volume Rate of Change
        vroc = ((volume - volume.shift(12)) / volume.shift(12)) * 100
        current['vroc'] = float(vroc.iloc[-1]) if not pd.isna(vroc.iloc[-1]) else None
        
        # Accumulation/Distribution Line
        ad_line = calculate_ad_line(high, low, close, volume)
        current['ad_line'] = float(ad_line.iloc[-1]) if not pd.isna(ad_line.iloc[-1]) else None

    # === SUPPORT/RESISTANCE ===
    if len(hist) >= 20:
        support_resistance = calculate_support_resistance(high, low, close, 20)
        current.update(support_resistance)

    return {"current": current}

def calculate_atr(high, low, close, period):
    """Calculate Average True Range."""
    high_low = high - low
    high_close = np.abs(high - close.shift())
    low_close = np.abs(low - close.shift())
    true_range = np.maximum(high_low, np.maximum(high_close, low_close))
    return true_range.rolling(window=period).mean()

def calculate_obv(close, volume):
    """Calculate On-Balance Volume."""
    obv = np.zeros(len(close))
    obv[0] = volume.iloc[0]
    
    for i in range(1, len(close)):
        if close.iloc[i] > close.iloc[i-1]:
            obv[i] = obv[i-1] + volume.iloc[i]
        elif close.iloc[i] < close.iloc[i-1]:
            obv[i] = obv[i-1] - volume.iloc[i]
        else:
            obv[i] = obv[i-1]
    
    return pd.Series(obv, index=close.index)

def calculate_ad_line(high, low, close, volume):
    """Calculate Accumulation/Distribution Line."""
    clv = ((close - low) - (high - close)) / (high - low)
    clv = clv.fillna(0)  # Handle division by zero
    ad_line = (clv * volume).cumsum()
    return ad_line

def calculate_support_resistance(high, low, close, lookback):
    """Calculate key support and resistance levels."""
    recent_high = high.tail(lookback).max()
    recent_low = low.tail(lookback).min()
    current_price = close.iloc[-1]
    
    # Calculate pivot points
    pivot = (recent_high + recent_low + current_price) / 3
    r1 = 2 * pivot - recent_low
    s1 = 2 * pivot - recent_high
    r2 = pivot + (recent_high - recent_low)
    s2 = pivot - (recent_high - recent_low)
    
    return {
        'support_1': float(s1),
        'support_2': float(s2),
        'resistance_1': float(r1),
        'resistance_2': float(r2),
        'pivot_point': float(pivot),
        'recent_high': float(recent_high),
        'recent_low': float(recent_low)
    }

def detect_patterns(hist):
    """Detect comprehensive chart and candlestick patterns for quantitative trading."""
    patterns = []
    if len(hist) < 10:
        return patterns
    
    close = hist['Close']
    high = hist['High']
    low = hist['Low']
    open_price = hist['Open']
    volume = hist['Volume'] if 'Volume' in hist.columns else None
    timestamp = datetime.now().isoformat()

    # === CANDLESTICK PATTERNS ===
    candlestick_patterns = detect_candlestick_patterns(open_price, high, low, close)
    patterns.extend(candlestick_patterns)

    # === CHART PATTERNS ===
    chart_patterns = detect_chart_patterns(high, low, close)
    patterns.extend(chart_patterns)

    # === TREND PATTERNS ===
    trend_patterns = detect_trend_patterns(close, high, low)
    patterns.extend(trend_patterns)

    # === VOLUME PATTERNS ===
    if volume is not None:
        volume_patterns = detect_volume_patterns(close, volume)
        patterns.extend(volume_patterns)

    # === SUPPORT/RESISTANCE PATTERNS ===
    sr_patterns = detect_support_resistance_patterns(high, low, close)
    patterns.extend(sr_patterns)
    
    return patterns

def detect_candlestick_patterns(open_price, high, low, close):
    """Detect common candlestick patterns."""
    patterns = []
    timestamp = datetime.now().isoformat()
    
    if len(close) < 3:
        return patterns

    # Get last 3 candles for pattern detection
    o1, o2, o3 = open_price.iloc[-3], open_price.iloc[-2], open_price.iloc[-1]
    h1, h2, h3 = high.iloc[-3], high.iloc[-2], high.iloc[-1]
    l1, l2, l3 = low.iloc[-3], low.iloc[-2], low.iloc[-1]
    c1, c2, c3 = close.iloc[-3], close.iloc[-2], close.iloc[-1]

    # Doji Pattern
    body_size = abs(c3 - o3)
    total_range = h3 - l3
    if total_range > 0 and body_size / total_range < 0.1:
        patterns.append({
            "type": "Doji",
            "confidence": 75,
            "description": "Indecision pattern - market uncertainty",
            "timestamp": timestamp
        })

    # Hammer Pattern
    if (c3 > o3 and  # Bullish candle
        (h3 - max(o3, c3)) < (min(o3, c3) - l3) and  # Small upper shadow, long lower shadow
        (min(o3, c3) - l3) > 2 * body_size):  # Lower shadow at least 2x body
        patterns.append({
            "type": "Hammer",
            "confidence": 80,
            "description": "Bullish reversal pattern - potential bottom",
            "timestamp": timestamp
        })

    # Shooting Star Pattern
    if (o3 > c3 and  # Bearish candle
        (min(o3, c3) - l3) < (h3 - max(o3, c3)) and  # Small lower shadow, long upper shadow
        (h3 - max(o3, c3)) > 2 * body_size):  # Upper shadow at least 2x body
        patterns.append({
            "type": "Shooting Star",
            "confidence": 80,
            "description": "Bearish reversal pattern - potential top",
            "timestamp": timestamp
        })

    # Engulfing Patterns
    if len(close) >= 2:
        # Bullish Engulfing
        if (c2 < o2 and  # Previous bearish
            c3 > o3 and  # Current bullish
            o3 < c2 and  # Current open below previous close
            c3 > o2):  # Current close above previous open
            patterns.append({
                "type": "Bullish Engulfing",
                "confidence": 85,
                "description": "Strong bullish reversal signal",
                "timestamp": timestamp
            })

        # Bearish Engulfing
        if (c2 > o2 and  # Previous bullish
            c3 < o3 and  # Current bearish
            o3 > c2 and  # Current open above previous close
            c3 < o2):  # Current close below previous open
            patterns.append({
                "type": "Bearish Engulfing",
                "confidence": 85,
                "description": "Strong bearish reversal signal",
                "timestamp": timestamp
            })

    return patterns

def detect_chart_patterns(high, low, close):
    """Detect classic chart patterns."""
    patterns = []
    timestamp = datetime.now().isoformat()
    
    if len(close) < 20:
        return patterns

    # Get recent data for pattern detection
    recent_high = high.tail(20)
    recent_low = low.tail(20)
    recent_close = close.tail(20)

    # Head and Shoulders (simplified)
    if detect_head_shoulders(recent_high, recent_low):
        patterns.append({
            "type": "Head and Shoulders",
            "confidence": 70,
            "description": "Bearish reversal pattern - potential trend change",
            "timestamp": timestamp
        })

    # Double Top/Bottom
    double_pattern = detect_double_top_bottom(recent_high, recent_low)
    if double_pattern:
        patterns.append({
            "type": double_pattern,
            "confidence": 75,
            "description": f"Reversal pattern - {double_pattern.lower()} formation",
            "timestamp": timestamp
        })

    # Triangle Patterns
    triangle = detect_triangle_patterns(recent_high, recent_low)
    if triangle:
        patterns.append({
            "type": triangle,
            "confidence": 65,
            "description": f"Consolidation pattern - {triangle.lower()} triangle",
            "timestamp": timestamp
        })

    return patterns

def detect_trend_patterns(close, high, low):
    """Detect trend-based patterns."""
    patterns = []
    timestamp = datetime.now().isoformat()
    
    if len(close) < 10:
        return patterns

    # Higher Highs and Higher Lows (Uptrend)
    if detect_higher_highs_lows(high, low):
        patterns.append({
            "type": "Higher Highs/Lows",
            "confidence": 80,
            "description": "Strong uptrend structure - bullish momentum",
            "timestamp": timestamp
        })

    # Lower Highs and Lower Lows (Downtrend)
    elif detect_lower_highs_lows(high, low):
        patterns.append({
            "type": "Lower Highs/Lows",
            "confidence": 80,
            "description": "Strong downtrend structure - bearish momentum",
            "timestamp": timestamp
        })

    # Breakout Pattern
    if detect_breakout(close, high, low):
        patterns.append({
            "type": "Breakout",
            "confidence": 75,
            "description": "Price breaking out of consolidation - potential strong move",
            "timestamp": timestamp
        })

    return patterns

def detect_volume_patterns(close, volume):
    """Detect volume-based patterns."""
    patterns = []
    timestamp = datetime.now().isoformat()
    
    if len(close) < 10:
        return patterns

    # Volume Spike
    avg_volume = volume.tail(20).mean()
    recent_volume = volume.iloc[-1]
    
    if recent_volume > avg_volume * 2:
        patterns.append({
            "type": "Volume Spike",
            "confidence": 70,
            "description": f"Unusual volume activity - {recent_volume/avg_volume:.1f}x average",
            "timestamp": timestamp
        })

    # Volume Divergence
    price_change = (close.iloc[-1] - close.iloc[-5]) / close.iloc[-5]
    volume_change = (volume.tail(5).mean() - volume.tail(10).mean()) / volume.tail(10).mean()
    
    if price_change > 0.02 and volume_change < -0.1:  # Price up, volume down
        patterns.append({
            "type": "Volume Divergence",
            "confidence": 60,
            "description": "Price rising but volume declining - potential weakness",
            "timestamp": timestamp
        })

    return patterns

def detect_support_resistance_patterns(high, low, close):
    """Detect support and resistance level patterns."""
    patterns = []
    timestamp = datetime.now().isoformat()
    
    if len(close) < 20:
        return patterns

    # Test of Support/Resistance
    current_price = close.iloc[-1]
    recent_high = high.tail(20).max()
    recent_low = low.tail(20).min()
    
    # Near resistance
    if current_price > recent_high * 0.98:
        patterns.append({
            "type": "Resistance Test",
            "confidence": 70,
            "description": "Price testing key resistance level",
            "timestamp": timestamp
        })
    
    # Near support
    elif current_price < recent_low * 1.02:
        patterns.append({
            "type": "Support Test",
            "confidence": 70,
            "description": "Price testing key support level",
            "timestamp": timestamp
        })

    return patterns

# Helper functions for pattern detection
def detect_head_shoulders(high, low):
    """Detect head and shoulders pattern."""
    if len(high) < 10:
        return False
    
    # Find peaks
    peaks = []
    for i in range(1, len(high) - 1):
        if high.iloc[i] > high.iloc[i-1] and high.iloc[i] > high.iloc[i+1]:
            peaks.append((i, high.iloc[i]))
    
    if len(peaks) < 3:
        return False
    
    # Check if middle peak is highest (head)
    peaks = sorted(peaks, key=lambda x: x[0])[-3:]  # Last 3 peaks
    if peaks[1][1] > peaks[0][1] and peaks[1][1] > peaks[2][1]:
        return True
    
    return False

def detect_double_top_bottom(high, low):
    """Detect double top or double bottom pattern."""
    if len(high) < 10:
        return None
    
    # Find significant peaks and troughs
    peaks = []
    troughs = []
    
    for i in range(1, len(high) - 1):
        if high.iloc[i] > high.iloc[i-1] and high.iloc[i] > high.iloc[i+1]:
            peaks.append(high.iloc[i])
        if low.iloc[i] < low.iloc[i-1] and low.iloc[i] < low.iloc[i+1]:
            troughs.append(low.iloc[i])
    
    # Check for double top
    if len(peaks) >= 2:
        recent_peaks = peaks[-2:]
        if abs(recent_peaks[0] - recent_peaks[1]) / recent_peaks[0] < 0.02:  # Within 2%
            return "Double Top"
    
    # Check for double bottom
    if len(troughs) >= 2:
        recent_troughs = troughs[-2:]
        if abs(recent_troughs[0] - recent_troughs[1]) / recent_troughs[0] < 0.02:  # Within 2%
            return "Double Bottom"
    
    return None

def detect_triangle_patterns(high, low):
    """Detect triangle patterns."""
    if len(high) < 10:
        return None
    
    # Calculate trend lines (simplified)
    recent_high = high.tail(10)
    recent_low = low.tail(10)
    
    # Ascending triangle (flat resistance, rising support)
    resistance_level = recent_high.max()
    if recent_high.iloc[-1] > resistance_level * 0.98:  # Near resistance
        return "Ascending Triangle"
    
    # Descending triangle (flat support, falling resistance)
    support_level = recent_low.min()
    if recent_low.iloc[-1] < support_level * 1.02:  # Near support
        return "Descending Triangle"
    
    return None

def detect_higher_highs_lows(high, low):
    """Detect higher highs and higher lows pattern."""
    if len(high) < 6:
        return False
    
    recent_high = high.tail(6)
    recent_low = low.tail(6)
    
    # Check for at least 2 higher highs and 2 higher lows
    higher_highs = sum(1 for i in range(1, len(recent_high)) if recent_high.iloc[i] > recent_high.iloc[i-1])
    higher_lows = sum(1 for i in range(1, len(recent_low)) if recent_low.iloc[i] > recent_low.iloc[i-1])
    
    return higher_highs >= 2 and higher_lows >= 2

def detect_lower_highs_lows(high, low):
    """Detect lower highs and lower lows pattern."""
    if len(high) < 6:
        return False
    
    recent_high = high.tail(6)
    recent_low = low.tail(6)
    
    # Check for at least 2 lower highs and 2 lower lows
    lower_highs = sum(1 for i in range(1, len(recent_high)) if recent_high.iloc[i] < recent_high.iloc[i-1])
    lower_lows = sum(1 for i in range(1, len(recent_low)) if recent_low.iloc[i] < recent_low.iloc[i-1])
    
    return lower_highs >= 2 and lower_lows >= 2

def detect_breakout(close, high, low):
    """Detect breakout pattern."""
    if len(close) < 10:
        return False
    
    # Check if price broke above recent high or below recent low
    recent_high = high.tail(10).max()
    recent_low = low.tail(10).min()
    current_price = close.iloc[-1]
    
    return current_price > recent_high * 1.01 or current_price < recent_low * 0.99

def generate_signals(hist, technical_indicators):
    """Generate comprehensive trading signals for quantitative analysis."""
    signals = []
    current = technical_indicators.get('current', {}) if isinstance(technical_indicators, dict) else {}
    if not current:
        return signals

    close = hist['Close'].iloc[-1]
    high = hist['High'].iloc[-1]
    low = hist['Low'].iloc[-1]

    # === MOMENTUM SIGNALS (SHORT-TERM) ===
    
    # RSI Signals
    rsi = current.get('rsi')
    if rsi is not None:
        if rsi < 20:
            signals.append({
                "type": "BUY",
                "strength": "VERY_STRONG",
                "indicator": "RSI",
                "reason": f"Extreme oversold (RSI: {rsi:.1f})",
                "timeframe": "short"
            })
        elif rsi < 30:
            signals.append({
                "type": "BUY",
                "strength": "STRONG",
                "indicator": "RSI",
                "reason": f"Oversold condition (RSI: {rsi:.1f})",
                "timeframe": "short"
            })
        elif rsi > 80:
            signals.append({
                "type": "SELL",
                "strength": "VERY_STRONG",
                "indicator": "RSI",
                "reason": f"Extreme overbought (RSI: {rsi:.1f})",
                "timeframe": "short"
            })
        elif rsi > 70:
            signals.append({
                "type": "SELL",
                "strength": "STRONG",
                "indicator": "RSI",
                "reason": f"Overbought condition (RSI: {rsi:.1f})",
                "timeframe": "short"
            })

    # Stochastic Signals
    stoch_k = current.get('stoch_k')
    stoch_d = current.get('stoch_d')
    if stoch_k is not None and stoch_d is not None:
        if stoch_k < 20 and stoch_d < 20 and stoch_k > stoch_d:
            signals.append({
                "type": "BUY",
                "strength": "STRONG",
                "indicator": "Stochastic",
                "reason": f"Oversold with bullish crossover (K: {stoch_k:.1f}, D: {stoch_d:.1f})",
                "timeframe": "short"
            })
        elif stoch_k > 80 and stoch_d > 80 and stoch_k < stoch_d:
            signals.append({
                "type": "SELL",
                "strength": "STRONG",
                "indicator": "Stochastic",
                "reason": f"Overbought with bearish crossover (K: {stoch_k:.1f}, D: {stoch_d:.1f})",
                "timeframe": "short"
            })

    # Williams %R Signals
    williams_r = current.get('williams_r')
    if williams_r is not None:
        if williams_r < -80:
            signals.append({
                "type": "BUY",
                "strength": "STRONG",
                "indicator": "Williams %R",
                "reason": f"Oversold (Williams %R: {williams_r:.1f})",
                "timeframe": "short"
            })
        elif williams_r > -20:
            signals.append({
                "type": "SELL",
                "strength": "STRONG",
                "indicator": "Williams %R",
                "reason": f"Overbought (Williams %R: {williams_r:.1f})",
                "timeframe": "short"
            })

    # CCI Signals
    cci = current.get('cci')
    if cci is not None:
        if cci < -100:
            signals.append({
                "type": "BUY",
                "strength": "MEDIUM",
                "indicator": "CCI",
                "reason": f"Oversold (CCI: {cci:.1f})",
                "timeframe": "short"
            })
        elif cci > 100:
            signals.append({
                "type": "SELL",
                "strength": "MEDIUM",
                "indicator": "CCI",
                "reason": f"Overbought (CCI: {cci:.1f})",
                "timeframe": "short"
            })

    # === TREND SIGNALS (MEDIUM-TERM) ===
    
    # MACD Signals
    macd = current.get('macd')
    macd_signal = current.get('macd_signal')
    macd_histogram = current.get('macd_histogram')
    if macd is not None and macd_signal is not None:
        if macd > macd_signal and macd_histogram is not None and macd_histogram > 0:
            signals.append({
                "type": "BUY",
                "strength": "STRONG",
                "indicator": "MACD",
                "reason": f"Bullish crossover with positive histogram (MACD: {macd:.3f})",
                "timeframe": "medium"
            })
        elif macd < macd_signal and macd_histogram is not None and macd_histogram < 0:
            signals.append({
                "type": "SELL",
                "strength": "STRONG",
                "indicator": "MACD",
                "reason": f"Bearish crossover with negative histogram (MACD: {macd:.3f})",
                "timeframe": "medium"
            })

    # ADX Trend Strength
    adx = current.get('adx')
    plus_di = current.get('plus_di')
    minus_di = current.get('minus_di')
    if adx is not None and plus_di is not None and minus_di is not None:
        if adx > 25:  # Strong trend
            if plus_di > minus_di:
                signals.append({
                    "type": "BUY",
                    "strength": "MEDIUM",
                    "indicator": "ADX",
                    "reason": f"Strong uptrend (ADX: {adx:.1f}, +DI: {plus_di:.1f})",
                    "timeframe": "medium"
                })
            elif minus_di > plus_di:
                signals.append({
                    "type": "SELL",
                    "strength": "MEDIUM",
                    "indicator": "ADX",
                    "reason": f"Strong downtrend (ADX: {adx:.1f}, -DI: {minus_di:.1f})",
                    "timeframe": "medium"
                })
        elif adx < 20:
            signals.append({
                "type": "HOLD",
                "strength": "WEAK",
                "indicator": "ADX",
                "reason": f"Weak trend (ADX: {adx:.1f}) - sideways market",
                "timeframe": "medium"
            })

    # === MOVING AVERAGE SIGNALS (LONG-TERM) ===
    
    # SMA Crossovers
    sma_20 = current.get('sma_20')
    sma_50 = current.get('sma_50')
    sma_200 = current.get('sma_200')
    
    if sma_20 is not None and sma_50 is not None:
        if sma_20 > sma_50:
            signals.append({
                "type": "BUY",
                "strength": "MEDIUM",
                "indicator": "SMA Crossover",
                "reason": "Golden Cross (SMA20 > SMA50)",
                "timeframe": "long"
            })
        elif sma_20 < sma_50:
            signals.append({
                "type": "SELL",
                "strength": "MEDIUM",
                "indicator": "SMA Crossover",
                "reason": "Death Cross (SMA20 < SMA50)",
                "timeframe": "long"
            })

    # Price vs SMA200
    if sma_200 is not None:
        if close > sma_200:
            signals.append({
                "type": "BUY",
                "strength": "WEAK",
                "indicator": "SMA200",
                "reason": f"Price above long-term average ({close:.2f} > {sma_200:.2f})",
                "timeframe": "long"
            })
        else:
            signals.append({
                "type": "SELL",
                "strength": "WEAK",
                "indicator": "SMA200",
                "reason": f"Price below long-term average ({close:.2f} < {sma_200:.2f})",
                "timeframe": "long"
            })

    # === VOLATILITY SIGNALS ===
    
    # Bollinger Bands
    bb_upper = current.get('bb_upper')
    bb_lower = current.get('bb_lower')
    bb_percent = current.get('bb_percent')
    if bb_upper is not None and bb_lower is not None and bb_percent is not None:
        if bb_percent < 0.1:  # Near lower band
            signals.append({
                "type": "BUY",
                "strength": "MEDIUM",
                "indicator": "Bollinger Bands",
                "reason": f"Price near lower band ({bb_percent:.1%})",
                "timeframe": "short"
            })
        elif bb_percent > 0.9:  # Near upper band
            signals.append({
                "type": "SELL",
                "strength": "MEDIUM",
                "indicator": "Bollinger Bands",
                "reason": f"Price near upper band ({bb_percent:.1%})",
                "timeframe": "short"
            })

    # ATR-based signals
    atr = current.get('atr')
    if atr is not None:
        atr_percent = (atr / close) * 100
        if atr_percent > 3:  # High volatility
            signals.append({
                "type": "HOLD",
                "strength": "WEAK",
                "indicator": "ATR",
                "reason": f"High volatility detected ({atr_percent:.1f}%) - caution advised",
                "timeframe": "short"
            })

    # === VOLUME SIGNALS ===
    
    # Volume confirmation
    obv = current.get('obv')
    vroc = current.get('vroc')
    if obv is not None and vroc is not None:
        if vroc > 50:  # High volume growth
            signals.append({
                "type": "BUY",
                "strength": "MEDIUM",
                "indicator": "Volume",
                "reason": f"Strong volume growth ({vroc:.1f}%) - bullish confirmation",
                "timeframe": "medium"
            })
        elif vroc < -30:  # Volume decline
            signals.append({
                "type": "SELL",
                "strength": "WEAK",
                "indicator": "Volume",
                "reason": f"Volume declining ({vroc:.1f}%) - bearish signal",
                "timeframe": "medium"
            })

    # === SUPPORT/RESISTANCE SIGNALS ===
    
    # Pivot Point Signals
    pivot = current.get('pivot_point')
    resistance_1 = current.get('resistance_1')
    support_1 = current.get('support_1')
    
    if pivot is not None and resistance_1 is not None and support_1 is not None:
        if close > resistance_1:
            signals.append({
                "type": "BUY",
                "strength": "STRONG",
                "indicator": "Pivot Points",
                "reason": f"Price above R1 resistance ({close:.2f} > {resistance_1:.2f})",
                "timeframe": "short"
            })
        elif close < support_1:
            signals.append({
                "type": "SELL",
                "strength": "STRONG",
                "indicator": "Pivot Points",
                "reason": f"Price below S1 support ({close:.2f} < {support_1:.2f})",
                "timeframe": "short"
            })
    
    return signals

def calculate_risk_metrics(hist, technical_indicators):
    """Calculate comprehensive risk metrics for quantitative trading."""
    if len(hist) < 20:
        return {}
    
    close = hist['Close']
    high = hist['High']
    low = hist['Low']
    volume = hist['Volume'] if 'Volume' in hist.columns else None
    current = technical_indicators.get('current', {}) if isinstance(technical_indicators, dict) else {}
    
    risk_metrics = {}
    
    # === VOLATILITY METRICS ===
    
    # Historical Volatility (20-day)
    if len(close) >= 20:
        returns = close.pct_change().dropna()
        hv_20 = returns.tail(20).std() * np.sqrt(252)  # Annualized
        risk_metrics['historical_volatility_20d'] = float(hv_20 * 100)  # As percentage
    
    # ATR-based Volatility
    atr = current.get('atr')
    current_price = close.iloc[-1]
    if atr is not None:
        atr_percent = (atr / current_price) * 100
        risk_metrics['atr_percentage'] = float(atr_percent)
    
    # Bollinger Band Width
    bb_width = current.get('bb_width')
    if bb_width is not None:
        risk_metrics['bb_width_percentage'] = float(bb_width * 100)
    
    # === DRAWDOWN METRICS ===
    
    # Maximum Drawdown
    if len(close) >= 20:
        rolling_max = close.expanding().max()
        drawdown = (close - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        risk_metrics['max_drawdown'] = float(max_drawdown * 100)  # As percentage
        
        # Current Drawdown
        current_drawdown = drawdown.iloc[-1]
        risk_metrics['current_drawdown'] = float(current_drawdown * 100)
    
    # === MOMENTUM RISK METRICS ===
    
    # RSI Risk Assessment
    rsi = current.get('rsi')
    if rsi is not None:
        if rsi > 80:
            risk_metrics['rsi_risk'] = "EXTREME_OVERBOUGHT"
        elif rsi > 70:
            risk_metrics['rsi_risk'] = "OVERBOUGHT"
        elif rsi < 20:
            risk_metrics['rsi_risk'] = "EXTREME_OVERSOLD"
        elif rsi < 30:
            risk_metrics['rsi_risk'] = "OVERSOLD"
        else:
            risk_metrics['rsi_risk'] = "NEUTRAL"
    
    # ADX Trend Strength Risk
    adx = current.get('adx')
    if adx is not None:
        if adx > 50:
            risk_metrics['trend_strength'] = "VERY_STRONG"
        elif adx > 25:
            risk_metrics['trend_strength'] = "STRONG"
        elif adx > 15:
            risk_metrics['trend_strength'] = "MODERATE"
        else:
            risk_metrics['trend_strength'] = "WEAK"
    
    # === LIQUIDITY METRICS ===
    
    if volume is not None:
        # Average Volume
        avg_volume_20 = volume.tail(20).mean()
        risk_metrics['avg_volume_20d'] = float(avg_volume_20)
        
        # Volume Volatility
        volume_std = volume.tail(20).std()
        volume_cv = volume_std / avg_volume_20 if avg_volume_20 > 0 else 0
        risk_metrics['volume_volatility'] = float(volume_cv)
        
        # Recent Volume vs Average
        recent_volume = volume.iloc[-1]
        volume_ratio = recent_volume / avg_volume_20 if avg_volume_20 > 0 else 0
        risk_metrics['volume_ratio'] = float(volume_ratio)
    
    # === PRICE ACTION RISK ===
    
    # Price Range Analysis
    if len(close) >= 20:
        recent_high = high.tail(20).max()
        recent_low = low.tail(20).min()
        price_range = recent_high - recent_low
        range_percent = (price_range / current_price) * 100
        risk_metrics['price_range_percentage'] = float(range_percent)
        
        # Price Position in Range
        price_position = (current_price - recent_low) / (recent_high - recent_low) if recent_high > recent_low else 0.5
        risk_metrics['price_position_in_range'] = float(price_position)
    
    # === SUPPORT/RESISTANCE RISK ===
    
    # Distance to Key Levels
    support_1 = current.get('support_1')
    resistance_1 = current.get('resistance_1')
    
    if support_1 is not None:
        support_distance = ((current_price - support_1) / current_price) * 100
        risk_metrics['distance_to_support'] = float(support_distance)
    
    if resistance_1 is not None:
        resistance_distance = ((resistance_1 - current_price) / current_price) * 100
        risk_metrics['distance_to_resistance'] = float(resistance_distance)
    
    # === CORRELATION RISK (simplified) ===
    
    # Price vs Moving Averages
    sma_20 = current.get('sma_20')
    sma_50 = current.get('sma_50')
    sma_200 = current.get('sma_200')
    
    if sma_20 is not None and sma_50 is not None and sma_200 is not None:
        # Check if all MAs are aligned (trend confirmation)
        ma_aligned = (sma_20 > sma_50 > sma_200) or (sma_20 < sma_50 < sma_200)
        risk_metrics['ma_alignment'] = ma_aligned
        
        # MA Spread (indicates trend strength)
        ma_spread = ((sma_20 - sma_200) / sma_200) * 100
        risk_metrics['ma_spread_percentage'] = float(ma_spread)
    
    # === RISK SCORE CALCULATION ===
    
    # Calculate overall risk score (0-100, higher = riskier)
    risk_score = 0
    
    # Volatility component (0-30 points)
    if 'historical_volatility_20d' in risk_metrics:
        hv = risk_metrics['historical_volatility_20d']
        if hv > 50:
            risk_score += 30
        elif hv > 30:
            risk_score += 20
        elif hv > 20:
            risk_score += 10
    
    # Drawdown component (0-25 points)
    if 'max_drawdown' in risk_metrics:
        dd = abs(risk_metrics['max_drawdown'])
        if dd > 20:
            risk_score += 25
        elif dd > 15:
            risk_score += 20
        elif dd > 10:
            risk_score += 15
        elif dd > 5:
            risk_score += 10
    
    # RSI risk component (0-20 points)
    if 'rsi_risk' in risk_metrics:
        rsi_risk = risk_metrics['rsi_risk']
        if rsi_risk in ['EXTREME_OVERBOUGHT', 'EXTREME_OVERSOLD']:
            risk_score += 20
        elif rsi_risk in ['OVERBOUGHT', 'OVERSOLD']:
            risk_score += 10
    
    # Trend strength component (0-15 points)
    if 'trend_strength' in risk_metrics:
        trend = risk_metrics['trend_strength']
        if trend == 'WEAK':
            risk_score += 15
        elif trend == 'MODERATE':
            risk_score += 10
        elif trend == 'STRONG':
            risk_score += 5
    
    # Volume component (0-10 points)
    if 'volume_ratio' in risk_metrics:
        vol_ratio = risk_metrics['volume_ratio']
        if vol_ratio < 0.5:  # Low volume
            risk_score += 10
        elif vol_ratio < 0.8:
            risk_score += 5
    
    risk_metrics['overall_risk_score'] = min(100, risk_score)
    
    # Risk level classification
    if risk_score >= 80:
        risk_metrics['risk_level'] = "VERY_HIGH"
    elif risk_score >= 60:
        risk_metrics['risk_level'] = "HIGH"
    elif risk_score >= 40:
        risk_metrics['risk_level'] = "MEDIUM"
    elif risk_score >= 20:
        risk_metrics['risk_level'] = "LOW"
    else:
        risk_metrics['risk_level'] = "VERY_LOW"
    
    return risk_metrics

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

@router.get("/risk-metrics/{symbol}")
async def get_risk_metrics(symbol: str, timeframe: str = Query("1M", regex="^(1D|1W|1M|3M|6M|YTD|1Y)$")):
    """Get comprehensive risk metrics for quantitative trading analysis."""
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
    risk_metrics = calculate_risk_metrics(hist, indicators)
    return _to_builtin({"risk_metrics": risk_metrics})
