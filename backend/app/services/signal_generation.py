"""
Signal Generation Service

Generates comprehensive trading signals for quantitative analysis.
"""
import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


def generate_signals(hist: Any, technical_indicators: Dict) -> List[Dict[str, Any]]:
    """
    Generate comprehensive trading signals for quantitative analysis.

    Args:
        hist: Historical OHLCV data
        technical_indicators: Dictionary of calculated technical indicators

    Returns:
        List of signal dictionaries with type, strength, indicator, reason, and timeframe
    """
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
