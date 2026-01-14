"""
Market utilities - Shared functions for market data analysis.

This module contains common utilities used across market analysis services.
"""
import numpy as np
import pandas as pd
import yfinance as yf
import logging
from typing import Dict, Tuple, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


# Timeframe mapping for yfinance data fetching
# Maps UI timeframe selection to yfinance period and interval
TIMEFRAME_MAP: Dict[str, Tuple[str, str]] = {
    "1D": ("1d", "5m"),
    "1W": ("7d", "1h"),
    "1M": ("1mo", "1d"),
    "3M": ("3mo", "1d"),
    "6M": ("6mo", "1d"),
    "1Y": ("1y", "1d"),
    "YTD": ("ytd", "1d")
}


def _to_builtin(value: Any) -> Any:
    """
    Recursively convert numpy/pandas scalars to native Python types.

    This is necessary for JSON serialization of API responses.
    Handles NaN and Inf values by converting them to None.
    """
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        f = float(value)
        return None if not np.isfinite(f) else f
    if isinstance(value, (np.bool_,)):
        return bool(value)
    # Handle regular Python floats that might be NaN or Inf
    if isinstance(value, float):
        return None if (value != value or abs(value) == float('inf')) else value
    if isinstance(value, (list, tuple)):
        return [_to_builtin(v) for v in value]
    if isinstance(value, dict):
        return {k: _to_builtin(v) for k, v in value.items()}
    return value


def fetch_yfinance_data(symbol: str, timeframe: str = "1M") -> Optional[pd.DataFrame]:
    """
    Fetch market data from yfinance for a given symbol and timeframe.

    Args:
        symbol: Stock symbol (e.g., "AAPL")
        timeframe: Timeframe selection (1D, 1W, 1M, 3M, 6M, YTD, 1Y)

    Returns:
        DataFrame with OHLCV data or None if fetch fails

    Raises:
        ValueError: If symbol is empty or timeframe is invalid
    """
    if not symbol:
        raise ValueError("Symbol cannot be empty")

    period, interval = TIMEFRAME_MAP.get(timeframe, ("1mo", "1d"))

    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)

        if hist.empty:
            logger.warning(f"No data found for symbol {symbol} with timeframe {timeframe}")
            return None

        return hist

    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        return None


def get_market_data_info(ticker: yf.Ticker, hist: pd.DataFrame) -> Dict[str, Any]:
    """
    Extract basic market data information from yfinance ticker and history.

    Args:
        ticker: yfinance Ticker object
        hist: Historical data DataFrame

    Returns:
        Dictionary with market data including price, change, volume, etc.
    """
    info = ticker.info
    current_price = float(hist['Close'].iloc[-1])
    previous_price = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
    price_change = float(((current_price - previous_price) / previous_price) * 100) if previous_price else 0.0

    return {
        'symbol': ticker.ticker,
        'price': float(current_price),
        'change': float(current_price - previous_price),
        'change_percent': float(price_change),
        'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns and not pd.isna(hist['Volume'].iloc[-1]) else 0,
        'market_cap': int(info.get('marketCap') or 0),
        'pe_ratio': float(info.get('trailingPE') or 0),
        'high_52w': float(info.get('fiftyTwoWeekHigh') or 0),
        'low_52w': float(info.get('fiftyTwoWeekLow') or 0),
        'chart_data': [float(x) for x in hist['Close'].tolist()[-7:]]  # Last 7 data points
    }


def validate_timeframe(timeframe: str) -> bool:
    """
    Validate that a timeframe string is supported.

    Args:
        timeframe: Timeframe string to validate

    Returns:
        True if valid, False otherwise
    """
    return timeframe in TIMEFRAME_MAP


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()
