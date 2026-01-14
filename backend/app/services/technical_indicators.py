"""
Technical Indicators Service

Calculates comprehensive technical indicators for quantitative trading analysis.
"""
import numpy as np
import pandas as pd
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def calculate_technical_indicators(hist: pd.DataFrame) -> Dict[str, Dict]:
    """
    Calculate comprehensive technical indicators for quantitative trading.

    Args:
        hist: Historical OHLCV data from yfinance

    Returns:
        Dictionary with 'current' key containing all indicator values
    """
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


def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int) -> pd.Series:
    """
    Calculate Average True Range.

    ATR measures market volatility. It incorporates closing price, high, and low.
    """
    high_low = high - low
    high_close = np.abs(high - close.shift())
    low_close = np.abs(low - close.shift())
    true_range = np.maximum(high_low, np.maximum(high_close, low_close))
    return true_range.rolling(window=period).mean()


def calculate_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    """
    Calculate On-Balance Volume.

    OBV measures buying and selling pressure as a cumulative indicator.
    """
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


def calculate_ad_line(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series) -> pd.Series:
    """
    Calculate Accumulation/Distribution Line.

    A/D line measures the cumulative flow of money into and out of a security.
    """
    clv = ((close - low) - (high - close)) / (high - low)
    clv = clv.fillna(0)  # Handle division by zero
    ad_line = (clv * volume).cumsum()
    return ad_line


def calculate_support_resistance(high: pd.Series, low: pd.Series, close: pd.Series, lookback: int) -> Dict[str, float]:
    """
    Calculate key support and resistance levels using pivot points.

    Args:
        high: High prices
        low: Low prices
        close: Close prices
        lookback: Period for recent high/low calculation

    Returns:
        Dictionary with support, resistance, and pivot levels
    """
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
