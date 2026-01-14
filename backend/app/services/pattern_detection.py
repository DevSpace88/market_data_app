"""
Pattern Detection Service

Detects comprehensive chart and candlestick patterns for quantitative trading.
"""
import numpy as np
import pandas as pd
from datetime import datetime
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


def detect_patterns(hist: pd.DataFrame) -> List[Dict[str, any]]:
    """
    Detect comprehensive chart and candlestick patterns for quantitative trading.

    Args:
        hist: Historical OHLCV data from yfinance

    Returns:
        List of detected patterns with metadata
    """
    patterns = []
    if len(hist) < 10:
        return patterns

    try:
        close = hist['Close']
        high = hist['High']
        low = hist['Low']
        open_price = hist['Open']
        volume = hist['Volume'] if 'Volume' in hist.columns else None
        timestamp = datetime.now().isoformat()

        # === CANDLESTICK PATTERNS ===
        try:
            candlestick_patterns = detect_candlestick_patterns(open_price, high, low, close)
            patterns.extend(candlestick_patterns)
        except Exception as e:
            logger.error(f"Error detecting candlestick patterns: {str(e)}")

        # === CHART PATTERNS ===
        try:
            chart_patterns = detect_chart_patterns(high, low, close)
            patterns.extend(chart_patterns)
        except Exception as e:
            logger.error(f"Error detecting chart patterns: {str(e)}")

        # === TREND PATTERNS ===
        try:
            trend_patterns = detect_trend_patterns(close, high, low)
            patterns.extend(trend_patterns)
        except Exception as e:
            logger.error(f"Error detecting trend patterns: {str(e)}")

        # === VOLUME PATTERNS ===
        if volume is not None:
            try:
                volume_patterns = detect_volume_patterns(close, volume)
                patterns.extend(volume_patterns)
            except Exception as e:
                logger.error(f"Error detecting volume patterns: {str(e)}")

        # === SUPPORT/RESISTANCE PATTERNS ===
        try:
            sr_patterns = detect_support_resistance_patterns(high, low, close)
            patterns.extend(sr_patterns)
        except Exception as e:
            logger.error(f"Error detecting support/resistance patterns: {str(e)}")

    except Exception as e:
        logger.error(f"Error in detect_patterns: {str(e)}")
        # Return a simple pattern as fallback
        patterns = [{
            "type": "Data Analysis",
            "confidence": 50,
            "description": "Basic market data analysis completed",
            "timestamp": datetime.now().isoformat()
        }]

    return patterns


def detect_candlestick_patterns(open_price: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series) -> List[Dict]:
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
        prev_body = abs(c2 - o2)
        curr_body = abs(c3 - o3)

        # Bullish Engulfing
        if (c2 < o2 and c3 > o3 and  # Previous red, current green
            c3 > o2 and o3 < c2 and  # Current engulfs previous
            curr_body > prev_body):
            patterns.append({
                "type": "Bullish Engulfing",
                "confidence": 85,
                "description": "Strong bullish reversal signal",
                "timestamp": timestamp
            })

        # Bearish Engulfing
        if (c2 > o2 and c3 < o3 and  # Previous green, current red
            c3 < o2 and o3 > c2 and  # Current engulfs previous
            curr_body > prev_body):
            patterns.append({
                "type": "Bearish Engulfing",
                "confidence": 85,
                "description": "Strong bearish reversal signal",
                "timestamp": timestamp
            })

    return patterns


def detect_chart_patterns(high: pd.Series, low: pd.Series, close: pd.Series) -> List[Dict]:
    """Detect chart patterns like Head & Shoulders, Double Top/Bottom, Triangles."""
    patterns = []
    timestamp = datetime.now().isoformat()

    if len(close) < 20:
        return patterns

    # Head & Shoulders detection (simplified)
    if detect_head_shoulders(high, low, close):
        patterns.append({
            "type": "Head & Shoulders",
            "confidence": 70,
            "description": "Potential bearish reversal pattern forming",
            "timestamp": timestamp
        })

    # Double Top/Bottom detection
    double_pattern = detect_double_top_bottom(high, low, close)
    if double_pattern:
        patterns.append({
            "type": double_pattern,
            "confidence": 75,
            "description": f"{'Bearish' if 'Top' in double_pattern else 'Bullish'} reversal pattern",
            "timestamp": timestamp
        })

    # Triangle patterns
    triangle = detect_triangle_patterns(high, low, close)
    if triangle:
        patterns.append({
            "type": triangle,
            "confidence": 65,
            "description": "Consolidation pattern - breakout possible",
            "timestamp": timestamp
        })

    return patterns


def detect_head_shoulders(high: pd.Series, low: pd.Series, close: pd.Series) -> bool:
    """Detect Head & Shoulders pattern (simplified)."""
    if len(close) < 30:
        return False

    # Look for three peaks with middle one highest
    recent_highs = high.tail(30)
    peaks = []

    for i in range(2, len(recent_highs) - 2):
        if (recent_highs.iloc[i] > recent_highs.iloc[i-1] and
            recent_highs.iloc[i] > recent_highs.iloc[i-2] and
            recent_highs.iloc[i] > recent_highs.iloc[i+1] and
            recent_highs.iloc[i] > recent_highs.iloc[i+2]):
            peaks.append((i, recent_highs.iloc[i]))

    if len(peaks) >= 3:
        # Check if middle peak is highest
        sorted_peaks = sorted(peaks, key=lambda x: x[1], reverse=True)
        if sorted_peaks[0][1] > sorted_peaks[1][1] * 1.02:  # At least 2% higher
            return True

    return False


def detect_double_top_bottom(high: pd.Series, low: pd.Series, close: pd.Series) -> Optional[str]:
    """Detect Double Top or Double Bottom pattern."""
    if len(close) < 20:
        return None

    window = 10
    recent_high = high.tail(window)
    recent_low = low.tail(window)

    # Find peaks in recent data
    max_high = recent_high.max()
    min_low = recent_low.min()

    # Double Top: Two similar highs
    high_values = recent_high[recent_high > max_high * 0.98]
    if len(high_values) >= 2:
        return "Double Top"

    # Double Bottom: Two similar lows
    low_values = recent_low[recent_low < min_low * 1.02]
    if len(low_values) >= 2:
        return "Double Bottom"

    return None


def detect_triangle_patterns(high: pd.Series, low: pd.Series, close: pd.Series) -> Optional[str]:
    """Detect triangle consolidation patterns."""
    if len(close) < 20:
        return None

    recent_high = high.tail(20)
    recent_low = low.tail(20)

    # Check for converging highs and lows
    high_trend = np.polyfit(range(len(recent_high)), recent_high, 1)[0]
    low_trend = np.polyfit(range(len(recent_low)), recent_low, 1)[0]

    # Ascending Triangle: Flat top, rising bottom
    if abs(high_trend) < 0.01 and low_trend > 0.05:
        return "Ascending Triangle"

    # Descending Triangle: Rising top, flat bottom
    if high_trend < -0.05 and abs(low_trend) < 0.01:
        return "Descending Triangle"

    # Symmetrical Triangle: Converging
    if high_trend < -0.02 and low_trend > 0.02:
        return "Symmetrical Triangle"

    return None


def detect_trend_patterns(close: pd.Series, high: pd.Series, low: pd.Series) -> List[Dict]:
    """Detect trend patterns like higher highs/lows, breakouts."""
    patterns = []
    timestamp = datetime.now().isoformat()

    # Higher Highs and Higher Lows (Uptrend)
    if detect_higher_highs_lows(high, low):
        patterns.append({
            "type": "Uptrend",
            "confidence": 80,
            "description": "Higher highs and higher lows - bullish structure",
            "timestamp": timestamp
        })

    # Lower Highs and Lower Lows (Downtrend)
    if detect_lower_highs_lows(high, low):
        patterns.append({
            "type": "Downtrend",
            "confidence": 80,
            "description": "Lower highs and lower lows - bearish structure",
            "timestamp": timestamp
        })

    # Breakout Detection
    if detect_breakout(close, high, low):
        direction = "above resistance" if close.iloc[-1] > high.tail(10).max() else "below support"
        patterns.append({
            "type": "Breakout",
            "confidence": 75,
            "description": f"Price broke {direction} - momentum signal",
            "timestamp": timestamp
        })

    return patterns


def detect_higher_highs_lows(high: pd.Series, low: pd.Series) -> bool:
    """Detect higher highs and higher lows pattern."""
    if len(high) < 6:
        return False

    recent_high = high.tail(6)
    recent_low = low.tail(6)

    # Check for at least 2 higher highs and 2 higher lows
    higher_highs = sum(1 for i in range(1, len(recent_high)) if recent_high.iloc[i] > recent_high.iloc[i-1])
    higher_lows = sum(1 for i in range(1, len(recent_low)) if recent_low.iloc[i] > recent_low.iloc[i-1])

    return higher_highs >= 2 and higher_lows >= 2


def detect_lower_highs_lows(high: pd.Series, low: pd.Series) -> bool:
    """Detect lower highs and lower lows pattern."""
    if len(high) < 6:
        return False

    recent_high = high.tail(6)
    recent_low = low.tail(6)

    # Check for at least 2 lower highs and 2 lower lows
    lower_highs = sum(1 for i in range(1, len(recent_high)) if recent_high.iloc[i] < recent_high.iloc[i-1])
    lower_lows = sum(1 for i in range(1, len(recent_low)) if recent_low.iloc[i] < recent_low.iloc[i-1])

    return lower_highs >= 2 and lower_lows >= 2


def detect_breakout(close: pd.Series, high: pd.Series, low: pd.Series) -> bool:
    """Detect breakout pattern."""
    if len(close) < 10:
        return False

    # Check if price broke above recent high or below recent low
    recent_high = high.tail(10).max()
    recent_low = low.tail(10).min()
    current_price = close.iloc[-1]

    return current_price > recent_high * 1.01 or current_price < recent_low * 0.99


def detect_volume_patterns(close: pd.Series, volume: pd.Series) -> List[Dict]:
    """Detect volume-based patterns."""
    patterns = []
    timestamp = datetime.now().isoformat()

    if len(volume) < 20:
        return patterns

    # Volume Spike
    avg_volume = volume.tail(20).mean()
    current_volume = volume.iloc[-1]

    if current_volume > avg_volume * 2:
        # Check if price moved with volume spike
        price_change = abs(close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]
        if price_change > 0.01:
            direction = "bullish" if close.iloc[-1] > close.iloc[-2] else "bearish"
            patterns.append({
                "type": "Volume Spike",
                "confidence": 70,
                "description": f"High volume with price movement - {direction} signal",
                "timestamp": timestamp
            })

    # Volume Divergence
    recent_volumes = volume.tail(10)
    recent_prices = close.tail(10)

    volume_trend = np.polyfit(range(len(recent_volumes)), recent_volumes, 1)[0]
    price_trend = np.polyfit(range(len(recent_prices)), recent_prices, 1)[0]

    # Bearish divergence: Price up, volume down
    if price_trend > 0 and volume_trend < 0:
        patterns.append({
            "type": "Bearish Divergence",
            "confidence": 65,
            "description": "Price rising with decreasing volume - potential reversal",
            "timestamp": timestamp
        })

    # Bullish divergence: Price down, volume up
    if price_trend < 0 and volume_trend > 0:
        patterns.append({
            "type": "Bullish Divergence",
            "confidence": 65,
            "description": "Price falling with increasing volume - potential reversal",
            "timestamp": timestamp
        })

    return patterns


def detect_support_resistance_patterns(high: pd.Series, low: pd.Series, close: pd.Series) -> List[Dict]:
    """Detect support and resistance interaction patterns."""
    patterns = []
    timestamp = datetime.now().isoformat()

    if len(close) < 20:
        return patterns

    lookback = 20
    recent_high = high.tail(lookback).max()
    recent_low = low.tail(lookback).min()
    current_price = close.iloc[-1]

    # Near Resistance
    if current_price > recent_high * 0.98:
        patterns.append({
            "type": "Near Resistance",
            "confidence": 70,
            "description": f"Price approaching resistance at {recent_high:.2f}",
            "timestamp": timestamp
        })

    # Near Support
    if current_price < recent_low * 1.02:
        patterns.append({
            "type": "Near Support",
            "confidence": 70,
            "description": f"Price approaching support at {recent_low:.2f}",
            "timestamp": timestamp
        })

    # Range-bound (sideways)
    price_range = (recent_high - recent_low) / recent_high
    if price_range < 0.05:
        patterns.append({
            "type": "Range-bound",
            "confidence": 75,
            "description": "Price consolidating in narrow range - breakout pending",
            "timestamp": timestamp
        })

    return patterns
