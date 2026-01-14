"""
Risk Metrics Service

Calculates comprehensive risk metrics for quantitative trading.
"""
import numpy as np
import pandas as pd
import logging
from typing import Dict

logger = logging.getLogger(__name__)


def calculate_risk_metrics(hist: pd.DataFrame, technical_indicators: Dict) -> Dict[str, any]:
    """
    Calculate comprehensive risk metrics for quantitative trading.

    Args:
        hist: Historical OHLCV data
        technical_indicators: Dictionary of calculated technical indicators

    Returns:
        Dictionary with all calculated risk metrics
    """
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
        elif adx > 20:
            risk_metrics['trend_strength'] = "MODERATE"
        else:
            risk_metrics['trend_strength'] = "WEAK"

    # === LIQUIDITY METRICS ===

    if volume is not None:
        # Average Volume
        avg_volume = volume.tail(20).mean()
        risk_metrics['average_volume_20d'] = int(avg_volume)

        # Volume Volatility
        volume_returns = volume.pct_change().dropna()
        if len(volume_returns) > 0:
            volume_volatility = volume_returns.tail(20).std() * 100
            risk_metrics['volume_volatility'] = float(volume_volatility)

    # === PRICE ACTION RISK ===

    # Price Range Analysis
    if len(close) >= 20:
        recent_range = (high.tail(20).max() - low.tail(20).min()) / close.iloc[-1] * 100
        risk_metrics['price_range_20d'] = float(recent_range)

    # Gap Risk (difference between open and previous close)
    if 'Open' in hist.columns and len(hist) >= 2:
        open_price = hist['Open'].iloc[-1]
        prev_close = close.iloc[-2]
        gap = abs(open_price - prev_close) / prev_close * 100
        risk_metrics['gap_percentage'] = float(gap)

    # === COMPOSITE RISK SCORE ===

    risk_score = calculate_composite_risk_score(risk_metrics, current, current_price)
    risk_metrics['overall_risk_score'] = risk_score
    risk_metrics['risk_level'] = get_risk_level(risk_score)

    # === ADDITIONAL RISK INDICATORS ===

    # Volatility Regime Detection
    if 'historical_volatility_20d' in risk_metrics:
        hv = risk_metrics['historical_volatility_20d']
        if hv > 50:
            risk_metrics['volatility_regime'] = "EXTREME"
        elif hv > 35:
            risk_metrics['volatility_regime'] = "HIGH"
        elif hv > 20:
            risk_metrics['volatility_regime'] = "MODERATE"
        else:
            risk_metrics['volatility_regime'] = "LOW"

    # Drawdown Status
    if 'current_drawdown' in risk_metrics:
        dd = risk_metrics['current_drawdown']
        if dd < -20:
            risk_metrics['drawdown_status'] = "SEVERE"
        elif dd < -10:
            risk_metrics['drawdown_status'] = "HIGH"
        elif dd < -5:
            risk_metrics['drawdown_status'] = "MODERATE"
        else:
            risk_metrics['drawdown_status'] = "NORMAL"

    return risk_metrics


def calculate_composite_risk_score(risk_metrics: Dict, current_indicators: Dict, current_price: float) -> int:
    """
    Calculate a composite risk score from 0 to 100.

    Higher score = higher risk

    Args:
        risk_metrics: Dictionary of calculated risk metrics
        current_indicators: Current technical indicators
        current_price: Current price

    Returns:
        Risk score from 0-100
    """
    score = 0

    # Volatility contribution (0-30 points)
    hv = risk_metrics.get('historical_volatility_20d', 0)
    score += min(hv / 2, 30)  # 50% volatility = max points

    # Drawdown contribution (0-25 points)
    dd = risk_metrics.get('current_drawdown', 0)
    score += min(abs(dd) * 2, 25)  # 12.5% drawdown = max points

    # RSI extreme contribution (0-15 points)
    rsi = current_indicators.get('rsi', 50)
    if rsi > 80:
        score += 15
    elif rsi > 70:
        score += 10
    elif rsi < 20:
        score += 15
    elif rsi < 30:
        score += 10

    # ATR contribution (0-15 points)
    atr_pct = risk_metrics.get('atr_percentage', 0)
    score += min(atr_pct * 2, 15)

    # Trend strength contribution (0-15 points)
    adx = current_indicators.get('adx', 20)
    if adx > 50:
        score += 5  # Very strong trend = lower risk (reduced score)
    elif adx < 20:
        score += 15  # Weak trend = higher risk

    return min(int(score), 100)


def get_risk_level(risk_score: int) -> str:
    """
    Get risk level description from risk score.

    Args:
        risk_score: Risk score from 0-100

    Returns:
        Risk level description
    """
    if risk_score >= 70:
        return "VERY_HIGH"
    elif risk_score >= 50:
        return "HIGH"
    elif risk_score >= 30:
        return "MODERATE"
    elif risk_score >= 15:
        return "LOW"
    else:
        return "VERY_LOW"
