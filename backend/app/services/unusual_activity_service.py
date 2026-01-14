"""
Unusual Activity Detection Service

Detects unusual market activity that may indicate institutional moves:
- Volume spikes
- Unusual options activity (Phase 2)
- Dark pool activity (Phase 2)
- Price anomalies
"""
import logging
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class UnusualActivityService:
    """
    Detects unusual market activity using statistical analysis.
    Flags activity that deviates significantly from normal patterns.
    """

    # Thresholds for detection
    VOLUME_SPIKE_THRESHOLD = 3.0  # 3x standard deviations
    PRICE_ANOMALY_THRESHOLD = 2.5  # 2.5x standard deviations
    MIN_HISTORY_DAYS = 30  # Minimum days for baseline calculation

    def __init__(self, db: Session):
        self.db = db
        self.logger = logger
        self.cache = {}
        self.cache_duration = timedelta(minutes=1)  # Real-time, short cache

    async def detect_unusual_activity(
        self,
        symbol: str,
        market_data: List[Dict[str, Any]],
        current_price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Detect unusual activity for a symbol.

        Args:
            symbol: Stock symbol
            market_data: Historical OHLCV data
            current_price: Current price (optional, defaults to last close)

        Returns:
            Dict with detected activities and severity levels
        """
        try:
            if not market_data or len(market_data) < self.MIN_HISTORY_DAYS:
                return self._get_insufficient_data_response(symbol)

            # Check cache (very short cache for real-time data)
            cache_key = f"activity_{symbol}"
            if cache_key in self.cache:
                cached = self.cache[cache_key]
                if datetime.now() - cached['timestamp'] < self.cache_duration:
                    return cached['data']

            # Analyze data
            activities = []

            # Volume spike detection
            volume_activity = self._detect_volume_spike(market_data)
            if volume_activity:
                activities.append(volume_activity)

            # Price anomaly detection
            price_activity = self._detect_price_anomaly(market_data, current_price)
            if price_activity:
                activities.append(price_activity)

            # Build response
            has_activity = len(activities) > 0

            response = {
                "symbol": symbol,
                "has_unusual_activity": has_activity,
                "activities": activities,
                "overall_severity": self._calculate_overall_severity(activities),
                "timestamp": datetime.now().isoformat()
            }

            # Cache response
            self.cache[cache_key] = {
                'data': response,
                'timestamp': datetime.now()
            }

            return response

        except Exception as e:
            self.logger.error(f"Error detecting unusual activity: {e}")
            return self._get_error_response(symbol)

    def _detect_volume_spike(self, market_data: List[Dict]) -> Optional[Dict[str, Any]]:
        """Detect unusual volume spikes"""
        try:
            # Extract volumes
            volumes = [data.get('volume', 0) for data in market_data]
            volumes = [v for v in volumes if v > 0]

            if len(volumes) < self.MIN_HISTORY_DAYS:
                return None

            # Calculate statistics
            mean_volume = np.mean(volumes[:-1])  # Exclude current (last) volume
            std_volume = np.std(volumes[:-1])
            current_volume = volumes[-1]

            # Check for spike
            if std_volume > 0:
                z_score = (current_volume - mean_volume) / std_volume
            else:
                z_score = 0

            if z_score >= self.VOLUME_SPIKE_THRESHOLD:
                # Calculate severity
                ratio = current_volume / mean_volume if mean_volume > 0 else 1

                return {
                    "type": "VOLUME_SPIKE",
                    "severity": self._get_severity_level(z_score, threshold=self.VOLUME_SPIKE_THRESHOLD),
                    "confidence": min(100, int(z_score * 20)),
                    "details": {
                        "current_volume": int(current_volume),
                        "average_volume": int(mean_volume),
                        "ratio": round(ratio, 2),
                        "z_score": round(z_score, 2),
                        "deviation": f"{z_score:.1f}σ from mean"
                    },
                    "price_at_detection": market_data[-1].get('close'),
                    "timestamp": market_data[-1].get('timestamp'),
                    "interpretation": self._interpret_volume_spike(ratio, market_data)
                }

            return None

        except Exception as e:
            self.logger.error(f"Error detecting volume spike: {e}")
            return None

    def _detect_price_anomaly(
        self,
        market_data: List[Dict],
        current_price: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        """Detect unusual price movements"""
        try:
            # Use provided current price or last close
            if current_price is None:
                current_price = market_data[-1].get('close', 0)

            if current_price == 0:
                return None

            # Calculate price changes
            closes = [data.get('close', 0) for data in market_data[:-1]]
            closes = [c for c in closes if c > 0]

            if len(closes) < self.MIN_HISTORY_DAYS:
                return None

            # Calculate statistics
            mean_price = np.mean(closes)
            std_price = np.std(closes)

            if std_price == 0:
                return None

            # Check for anomaly
            z_score = abs(current_price - mean_price) / std_price

            if z_score >= self.PRICE_ANOMALY_THRESHOLD:
                # Calculate daily change
                prev_close = closes[-1]
                daily_change = ((current_price - prev_close) / prev_close) * 100 if prev_close > 0 else 0

                return {
                    "type": "PRICE_ANOMALY",
                    "severity": self._get_severity_level(z_score, threshold=self.PRICE_ANOMALY_THRESHOLD),
                    "confidence": min(100, int(z_score * 20)),
                    "details": {
                        "current_price": round(current_price, 2),
                        "average_price": round(mean_price, 2),
                        "daily_change_percent": round(daily_change, 2),
                        "z_score": round(z_score, 2),
                        "deviation": f"{z_score:.1f}σ from mean"
                    },
                    "timestamp": market_data[-1].get('timestamp'),
                    "interpretation": self._interpret_price_anomaly(daily_change, z_score)
                }

            return None

        except Exception as e:
            self.logger.error(f"Error detecting price anomaly: {e}")
            return None

    def _get_severity_level(self, z_score: float, threshold: float) -> str:
        """Determine severity level based on z-score"""
        if z_score >= threshold * 3:
            return "EXTREME"
        elif z_score >= threshold * 2:
            return "HIGH"
        elif z_score >= threshold:
            return "MEDIUM"
        else:
            return "LOW"

    def _interpret_volume_spike(self, ratio: float, market_data: List[Dict]) -> str:
        """Generate human-readable interpretation of volume spike"""
        # Check price movement with volume
        current_close = market_data[-1].get('close', 0)
        prev_close = market_data[-2].get('close', 0) if len(market_data) > 1 else current_close

        price_change = ((current_close - prev_close) / prev_close) * 100 if prev_close > 0 else 0

        if ratio >= 5:
            if price_change > 2:
                return "Massive volume spike with strong upward price movement - possible breakout or institutional accumulation"
            elif price_change < -2:
                return "Massive volume spike with strong downward price movement - possible breakdown or institutional distribution"
            else:
                return "Massive volume spike with little price movement - possible consolidation or battle between bulls and bears"

        elif ratio >= 3:
            if price_change > 1:
                return "Significant volume spike with upward price movement - bullish signal"
            elif price_change < -1:
                return "Significant volume spike with downward price movement - bearish signal"
            else:
                return "Significant volume spike - monitoring for direction"

        else:
            if price_change > 0:
                return f"Above-average volume ({ratio:.1f}x normal) with price gain"
            else:
                return f"Above-average volume ({ratio:.1f}x normal) with price decline"

    def _interpret_price_anomaly(self, daily_change: float, z_score: float) -> str:
        """Generate human-readable interpretation of price anomaly"""
        if abs(daily_change) >= 5:
            direction = "surge" if daily_change > 0 else "plunge"
            return f"Extreme price {direction} of {abs(daily_change):.1f}% - highly unusual movement"

        elif abs(daily_change) >= 3:
            direction = "rise" if daily_change > 0 else "fall"
            return f"Significant price {direction} of {abs(daily_change):.1f}% - notable deviation"

        else:
            return f"Price deviates {z_score:.1f} standard deviations from mean"

    def _calculate_overall_severity(self, activities: List[Dict]) -> str:
        """Calculate overall severity from all activities"""
        if not activities:
            return "NONE"

        severity_weights = {"EXTREME": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}

        max_weight = max(
            (severity_weights.get(a.get("severity", "LOW"), 1) for a in activities),
            default=0
        )

        if max_weight >= 4:
            return "EXTREME"
        elif max_weight >= 3:
            return "HIGH"
        elif max_weight >= 2:
            return "MEDIUM"
        else:
            return "LOW"

    def _get_insufficient_data_response(self, symbol: str) -> Dict[str, Any]:
        """Return response when insufficient data"""
        return {
            "symbol": symbol,
            "has_unusual_activity": False,
            "activities": [],
            "overall_severity": "NONE",
            "timestamp": datetime.now().isoformat(),
            "warning": f"Insufficient data for unusual activity detection (need {self.MIN_HISTORY_DAYS}+ days)"
        }

    def _get_error_response(self, symbol: str) -> Dict[str, Any]:
        """Return error response"""
        return {
            "symbol": symbol,
            "has_unusual_activity": False,
            "activities": [],
            "overall_severity": "ERROR",
            "timestamp": datetime.now().isoformat(),
            "error": "Unusual activity detection temporarily unavailable"
        }
