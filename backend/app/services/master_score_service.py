"""
Master Investment Score Service

Combines all technical indicators, risk metrics, patterns, and signals
into a single comprehensive score (0-100) with buy/sell/hold recommendation.
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class MasterScoreService:
    """
    Calculates a master investment score (0-100) based on multiple factors.

    Weight breakdown:
    - Short-term signals (30%): RSI, Stochastic, Williams %R, CCI
    - Medium-term signals (30%): MACD, ADX, SMA crossovers
    - Long-term signals (20%): Trends, Support/Resistance, SMA200
    - Risk metrics (20%): Volatility, Drawdown, Liquidity
    """

    # Score weights configuration
    WEIGHTS = {
        "short_term": 0.30,
        "medium_term": 0.30,
        "long_term": 0.20,
        "risk": 0.20,
    }

    # Score ranges for classification
    SCORE_RANGES = {
        "STRONG_SELL": (0, 20),
        "SELL": (20, 40),
        "HOLD": (40, 60),
        "BUY": (60, 80),
        "STRONG_BUY": (80, 100),
    }

    def __init__(self):
        self.logger = logger

    def calculate_master_score(
        self,
        technical_indicators: Dict,
        signals: List[Dict],
        risk_metrics: Optional[Dict] = None,
        patterns: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        Calculate the master investment score.

        Args:
            technical_indicators: Dict with 'current' indicators
            signals: List of trading signals
            risk_metrics: Optional risk metrics dict
            patterns: Optional detected patterns

        Returns:
            Dict with master_score, recommendation, confidence, and breakdown
        """
        try:
            current = technical_indicators.get('current', {})

            # Calculate component scores
            short_term_score = self._calculate_short_term_score(current, signals)
            medium_term_score = self._calculate_medium_term_score(current, signals)
            long_term_score = self._calculate_long_term_score(current, signals, patterns)
            risk_score = self._calculate_risk_score(risk_metrics, current)

            # Weighted final score
            final_score = (
                short_term_score * self.WEIGHTS["short_term"] +
                medium_term_score * self.WEIGHTS["medium_term"] +
                long_term_score * self.WEIGHTS["long_term"] +
                risk_score * self.WEIGHTS["risk"]
            )

            # Clamp to 0-100
            final_score = max(0, min(100, final_score))

            # Determine recommendation and confidence
            recommendation, confidence_level = self._get_recommendation(final_score, current)

            # Get top contributing factors
            top_factors = self._get_top_contributing_factors(
                short_term_score, medium_term_score, long_term_score, risk_score
            )

            return {
                "master_score": round(final_score, 2),
                "recommendation": recommendation,
                "confidence": confidence_level,
                "breakdown": {
                    "short_term": {
                        "score": round(short_term_score, 2),
                        "weight": self.WEIGHTS["short_term"],
                        "label": "Short-term (RSI, Stochastic, Williams %R)"
                    },
                    "medium_term": {
                        "score": round(medium_term_score, 2),
                        "weight": self.WEIGHTS["medium_term"],
                        "label": "Medium-term (MACD, ADX, SMA Crossovers)"
                    },
                    "long_term": {
                        "score": round(long_term_score, 2),
                        "weight": self.WEIGHTS["long_term"],
                        "label": "Long-term (Trends, Support/Resistance)"
                    },
                    "risk": {
                        "score": round(risk_score, 2),
                        "weight": self.WEIGHTS["risk"],
                        "label": "Risk Metrics (Volatility, Drawdown)"
                    }
                },
                "top_factors": top_factors,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error calculating master score: {e}")
            return self._get_error_response()

    def _calculate_short_term_score(self, current: Dict, signals: List[Dict]) -> float:
        """Calculate short-term score (0-100) based on momentum indicators"""
        score = 50.0  # Start neutral
        indicators_count = 0

        # RSI
        rsi = current.get('rsi')
        if rsi is not None:
            indicators_count += 1
            if rsi < 30:
                # Oversold = bullish
                score += min(25, (30 - rsi))
            elif rsi > 70:
                # Overbought = bearish
                score -= min(25, (rsi - 70))

        # Stochastic
        stoch_k = current.get('stoch_k')
        stoch_d = current.get('stoch_d')
        if stoch_k is not None and stoch_d is not None:
            indicators_count += 1
            if stoch_k < 20 and stoch_d < 20:
                score += 20  # Oversold
            elif stoch_k > 80 and stoch_d > 80:
                score -= 20  # Overbought
            elif stoch_k > stoch_d and stoch_k < 80:
                score += 10  # Bullish crossover
            elif stoch_k < stoch_d and stoch_k > 20:
                score -= 10  # Bearish crossover

        # Williams %R
        williams_r = current.get('williams_r')
        if williams_r is not None:
            indicators_count += 1
            if williams_r < -80:
                score += 15  # Oversold
            elif williams_r > -20:
                score -= 15  # Overbought

        # CCI
        cci = current.get('cci')
        if cci is not None:
            indicators_count += 1
            if cci < -100:
                score += 10  # Oversold
            elif cci > 100:
                score -= 10  # Overbought

        # Check short-term signals
        short_signals = [s for s in signals if s.get('timeframe') == 'short']
        for signal in short_signals:
            if signal.get('type') == 'BUY':
                score += {'WEAK': 5, 'MEDIUM': 10, 'STRONG': 15, 'VERY_STRONG': 20}.get(signal.get('strength'), 0)
            elif signal.get('type') == 'SELL':
                score -= {'WEAK': 5, 'MEDIUM': 10, 'STRONG': 15, 'VERY_STRONG': 20}.get(signal.get('strength'), 0)

        # Normalize if we have multiple indicators
        if indicators_count > 0:
            score = score / ((indicators_count * 0.2) + 0.8)

        return max(0, min(100, score))

    def _calculate_medium_term_score(self, current: Dict, signals: List[Dict]) -> float:
        """Calculate medium-term score (0-100) based on trend indicators"""
        score = 50.0  # Start neutral

        # MACD
        macd = current.get('macd')
        macd_signal = current.get('macd_signal')
        macd_histogram = current.get('macd_histogram')

        if macd is not None and macd_signal is not None:
            if macd > macd_signal:
                score += 15  # Bullish
                if macd_histogram and macd_histogram > 0:
                    score += 10  # Positive momentum
            else:
                score -= 15  # Bearish
                if macd_histogram and macd_histogram < 0:
                    score -= 10  # Negative momentum

        # ADX trend strength
        adx = current.get('adx')
        plus_di = current.get('plus_di')
        minus_di = current.get('minus_di')

        if adx is not None:
            if adx > 25:  # Strong trend
                if plus_di and minus_di:
                    if plus_di > minus_di:
                        score += 15  # Strong uptrend
                    else:
                        score -= 15  # Strong downtrend
            elif adx < 20:
                score -= 5  # Weak trend, uncertain

        # SMA Crossover (20/50)
        sma_20 = current.get('sma_20')
        sma_50 = current.get('sma_50')

        if sma_20 is not None and sma_50 is not None:
            if sma_20 > sma_50:
                score += 15  # Golden cross
            else:
                score -= 15  # Death cross

        # Check medium-term signals
        medium_signals = [s for s in signals if s.get('timeframe') == 'medium']
        for signal in medium_signals:
            if signal.get('type') == 'BUY':
                score += {'WEAK': 5, 'MEDIUM': 10, 'STRONG': 15, 'VERY_STRONG': 20}.get(signal.get('strength'), 0)
            elif signal.get('type') == 'SELL':
                score -= {'WEAK': 5, 'MEDIUM': 10, 'STRONG': 15, 'VERY_STRONG': 20}.get(signal.get('strength'), 0)

        return max(0, min(100, score))

    def _calculate_long_term_score(self, current: Dict, signals: List[Dict], patterns: Optional[List[Dict]]) -> float:
        """Calculate long-term score (0-100) based on long-term trends and patterns"""
        score = 50.0  # Start neutral

        # SMA200
        sma_200 = current.get('sma_200')
        current_price = current.get('close')  # If available

        if sma_200 is not None and current_price is not None:
            if current_price > sma_200:
                score += 20  # Above long-term average = bullish
            else:
                score -= 20  # Below long-term average = bearish

        # Check long-term signals
        long_signals = [s for s in signals if s.get('timeframe') == 'long']
        for signal in long_signals:
            if signal.get('type') == 'BUY':
                score += {'WEAK': 5, 'MEDIUM': 10, 'STRONG': 15, 'VERY_STRONG': 20}.get(signal.get('strength'), 0)
            elif signal.get('type') == 'SELL':
                score -= {'WEAK': 5, 'MEDIUM': 10, 'STRONG': 15, 'VERY_STRONG': 20}.get(signal.get('strength'), 0)

        # Pattern analysis (if available)
        if patterns:
            bullish_patterns = [p for p in patterns if any(word in p.get('type', '').lower() for word in ['bullish', 'hammer', 'morning star'])]
            bearish_patterns = [p for p in patterns if any(word in p.get('type', '').lower() for word in ['bearish', 'shooting star', 'evening star'])]

            if bullish_patterns:
                avg_confidence = sum(p.get('confidence', 0) for p in bullish_patterns) / len(bullish_patterns)
                score += (avg_confidence / 100) * 15

            if bearish_patterns:
                avg_confidence = sum(p.get('confidence', 0) for p in bearish_patterns) / len(bearish_patterns)
                score -= (avg_confidence / 100) * 15

        return max(0, min(100, score))

    def _calculate_risk_score(self, risk_metrics: Optional[Dict], current: Dict) -> float:
        """
        Calculate risk score (0-100).
        Higher score = lower risk (better).
        """
        if not risk_metrics:
            # Default to neutral if no risk metrics available
            return 50.0

        score = 50.0  # Start neutral

        # Volatility
        volatility = risk_metrics.get('volatility_score')
        if volatility is not None:
            # Lower volatility = higher score
            score += (100 - volatility) * 0.3

        # Drawdown
        drawdown = risk_metrics.get('drawdown')
        if drawdown is not None:
            # Lower drawdown = higher score
            score += (100 - abs(drawdown)) * 0.3

        # Liquidity risk
        liquidity = risk_metrics.get('liquidity_risk')
        if liquidity is not None:
            # Lower liquidity risk = higher score
            score += (100 - liquidity) * 0.2

        # Overall risk score
        overall_risk = risk_metrics.get('overall_risk_score')
        if overall_risk is not None:
            # Invert: lower risk = higher score
            score += (100 - overall_risk) * 0.2

        # ATR (Average True Range) - volatility indicator
        atr = current.get('atr')
        close = current.get('close')
        if atr is not None and close is not None and close > 0:
            atr_percent = (atr / close) * 100
            # Lower ATR % = lower volatility = higher score
            if atr_percent < 1:
                score += 10
            elif atr_percent > 3:
                score -= 10

        return max(0, min(100, score))

    def _get_recommendation(self, score: float, current: Dict) -> tuple[str, str]:
        """
        Get recommendation and confidence level based on score.

        Returns:
            Tuple of (recommendation, confidence_level)
        """
        # Determine recommendation
        if score >= 80:
            recommendation = "STRONG_BUY"
        elif score >= 60:
            recommendation = "BUY"
        elif score >= 40:
            recommendation = "HOLD"
        elif score >= 20:
            recommendation = "SELL"
        else:
            recommendation = "STRONG_SELL"

        # Determine confidence based on data availability
        available_indicators = sum(1 for v in current.values() if v is not None)
        total_indicators = len(current)

        if total_indicators > 0:
            data_quality = available_indicators / total_indicators
            if data_quality >= 0.8:
                confidence_level = "HIGH"
            elif data_quality >= 0.5:
                confidence_level = "MEDIUM"
            else:
                confidence_level = "LOW"
        else:
            confidence_level = "LOW"

        return recommendation, confidence_level

    def _get_top_contributing_factors(
        self,
        short_term: float,
        medium_term: float,
        long_term: float,
        risk: float
    ) -> List[Dict[str, Any]]:
        """Get top 3 factors contributing to the score"""
        factors = [
            {"name": "Short-term Momentum", "score": short_term, "weight": self.WEIGHTS["short_term"]},
            {"name": "Medium-term Trend", "score": medium_term, "weight": self.WEIGHTS["medium_term"]},
            {"name": "Long-term Trend", "score": long_term, "weight": self.WEIGHTS["long_term"]},
            {"name": "Risk Metrics", "score": risk, "weight": self.WEIGHTS["risk"]},
        ]

        # Sort by absolute deviation from 50 (neutral)
        factors.sort(key=lambda x: abs(x["score"] - 50) * x["weight"], reverse=True)

        # Return top 3
        return [
            {
                "name": f["name"],
                "score": round(f["score"], 2),
                "contribution": round((f["score"] - 50) * f["weight"], 2)
            }
            for f in factors[:3]
        ]

    def _get_error_response(self) -> Dict[str, Any]:
        """Return error response"""
        return {
            "master_score": 50.0,
            "recommendation": "HOLD",
            "confidence": "LOW",
            "breakdown": {
                "short_term": {"score": 50.0, "weight": 0.30, "label": "Short-term"},
                "medium_term": {"score": 50.0, "weight": 0.30, "label": "Medium-term"},
                "long_term": {"score": 50.0, "weight": 0.20, "label": "Long-term"},
                "risk": {"score": 50.0, "weight": 0.20, "label": "Risk"}
            },
            "top_factors": [],
            "error": "Unable to calculate master score",
            "timestamp": datetime.now().isoformat()
        }
