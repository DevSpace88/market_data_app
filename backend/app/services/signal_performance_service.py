"""
Signal Performance Tracking Service

Tracks and analyzes historical performance of generated signals.
Calculates win-rates, average returns, and benchmark comparisons.
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from ..models.investment_engine import SignalPerformance

logger = logging.getLogger(__name__)


class SignalPerformanceService:
    """
    Tracks signal performance and provides accuracy metrics.
    """

    def __init__(self, db: Session):
        self.db = db
        self.logger = logger

    def save_signal(
        self,
        symbol: str,
        signal_type: str,
        signal_strength: str,
        master_score: float,
        technical_score: Optional[float] = None,
        sentiment_score: Optional[float] = None,
        activity_score: Optional[float] = None,
    ) -> SignalPerformance:
        """Save a generated signal to the database for later evaluation"""
        try:
            signal = SignalPerformance(
                symbol=symbol,
                signal_type=signal_type,
                signal_strength=signal_strength,
                master_score=master_score,
                technical_score=technical_score,
                sentiment_score=sentiment_score,
                activity_score=activity_score,
                generated_at=datetime.now(),
                is_pending=True
            )

            self.db.add(signal)
            self.db.commit()
            self.db.refresh(signal)

            self.logger.info(f"Saved signal for {symbol}: {signal_type} ({signal_strength})")
            return signal

        except Exception as e:
            self.logger.error(f"Error saving signal: {e}")
            self.db.rollback()
            return None

    def evaluate_pending_signals(
        self,
        symbol: str,
        current_price: float,
        benchmark_return: float
    ) -> int:
        """
        Evaluate pending signals for a symbol.

        Args:
            symbol: Stock symbol
            current_price: Current price of the stock
            benchmark_return: Return of benchmark (e.g., S&P 500) over the period

        Returns:
            Number of signals evaluated
        """
        try:
            # Get pending signals older than 1 day
            cutoff_date = datetime.now() - timedelta(days=1)

            pending_signals = self.db.query(SignalPerformance).filter(
                and_(
                    SignalPerformance.symbol == symbol,
                    SignalPerformance.is_pending == True,
                    SignalPerformance.generated_at < cutoff_date
                )
            ).all()

            evaluated_count = 0

            for signal in pending_signals:
                # Calculate days since generation
                days_elapsed = (datetime.now() - signal.generated_at).days

                # Determine which timeframe to evaluate
                timeframe_days = self._get_evaluation_timeframe(days_elapsed)

                if timeframe_days:
                    # Get the price at signal generation (from stored data or historical)
                    # For now, we'll use a simplified approach
                    # In production, you'd store the price at generation

                    # Calculate return
                    # Note: This is simplified - you'd need the price at generation
                    # For now, skip actual return calculation

                    signal.timeframe_days = timeframe_days
                    signal.evaluated_at = datetime.now()
                    # signal.return_percent = calculated_return
                    signal.benchmark_return_percent = benchmark_return
                    # signal.excess_return = signal.return_percent - benchmark_return
                    # signal.is_profitable = signal.return_percent > 0
                    signal.is_pending = False

                    evaluated_count += 1

            self.db.commit()
            self.logger.info(f"Evaluated {evaluated_count} signals for {symbol}")
            return evaluated_count

        except Exception as e:
            self.logger.error(f"Error evaluating signals: {e}")
            self.db.rollback()
            return 0

    def get_accuracy_metrics(
        self,
        symbol: Optional[str] = None,
        signal_type: Optional[str] = None,
        timeframe_days: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get accuracy metrics for signals.

        Args:
            symbol: Filter by symbol (optional)
            signal_type: Filter by signal type (optional)
            timeframe_days: Filter by timeframe in days (optional)

        Returns:
            Dict with accuracy metrics
        """
        try:
            # Build query
            query = self.db.query(SignalPerformance).filter(
                SignalPerformance.is_pending == False
            )

            if symbol:
                query = query.filter(SignalPerformance.symbol == symbol)
            if signal_type:
                query = query.filter(SignalPerformance.signal_type == signal_type)
            if timeframe_days:
                query = query.filter(SignalPerformance.timeframe_days == timeframe_days)

            signals = query.all()

            if not signals:
                return self._get_no_metrics_response()

            # Calculate metrics
            total_signals = len(signals)
            profitable_signals = sum(1 for s in signals if s.is_profitable)

            win_rate = (profitable_signals / total_signals * 100) if total_signals > 0 else 0

            # Average returns
            avg_return = sum(s.return_percent or 0 for s in signals) / total_signals
            avg_benchmark_return = sum(s.benchmark_return_percent or 0 for s in signals) / total_signals
            avg_excess_return = sum(s.excess_return or 0 for s in signals) / total_signals

            # By signal type
            by_type = {}
            for sig_type in ["BUY", "SELL", "HOLD"]:
                type_signals = [s for s in signals if s.signal_type == sig_type]
                if type_signals:
                    type_profitable = sum(1 for s in type_signals if s.is_profitable)
                    by_type[sig_type] = {
                        "count": len(type_signals),
                        "win_rate": round((type_profitable / len(type_signals) * 100), 2),
                        "avg_return": round(sum(s.return_percent or 0 for s in type_signals) / len(type_signals), 2)
                    }

            # By timeframe
            by_timeframe = {}
            for tf in [1, 7, 30]:
                tf_signals = [s for s in signals if s.timeframe_days == tf]
                if tf_signals:
                    tf_profitable = sum(1 for s in tf_signals if s.is_profitable)
                    by_timeframe[f"{tf}D"] = {
                        "count": len(tf_signals),
                        "win_rate": round((tf_profitable / len(tf_signals) * 100), 2),
                        "avg_return": round(sum(s.return_percent or 0 for s in tf_signals) / len(tf_signals), 2)
                    }

            return {
                "overall": {
                    "total_signals": total_signals,
                    "profitable_signals": profitable_signals,
                    "win_rate": round(win_rate, 2),
                    "avg_return_percent": round(avg_return, 2),
                    "avg_benchmark_return_percent": round(avg_benchmark_return, 2),
                    "avg_excess_return_percent": round(avg_excess_return, 2)
                },
                "by_signal_type": by_type,
                "by_timeframe": by_timeframe,
                "vs_benchmark": {
                    "outperformed": sum(1 for s in signals if (s.excess_return or 0) > 0),
                    "underperformed": sum(1 for s in signals if (s.excess_return or 0) < 0),
                    "beat_rate": round((sum(1 for s in signals if (s.excess_return or 0) > 0) / total_signals * 100), 2)
                },
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error getting accuracy metrics: {e}")
            return self._get_error_response()

    def get_signal_strength_accuracy(self) -> Dict[str, Any]:
        """Get accuracy breakdown by signal strength"""
        try:
            signals = self.db.query(SignalPerformance).filter(
                SignalPerformance.is_pending == False
            ).all()

            if not signals:
                return {}

            by_strength = {}
            for strength in ["WEAK", "MEDIUM", "STRONG", "VERY_STRONG"]:
                strength_signals = [s for s in signals if s.signal_strength == strength]
                if strength_signals:
                    profitable = sum(1 for s in strength_signals if s.is_profitable)
                    by_strength[strength] = {
                        "count": len(strength_signals),
                        "win_rate": round((profitable / len(strength_signals) * 100), 2),
                        "avg_return": round(sum(s.return_percent or 0 for s in strength_signals) / len(strength_signals), 2)
                    }

            return by_strength

        except Exception as e:
            self.logger.error(f"Error getting strength accuracy: {e}")
            return {}

    def _get_evaluation_timeframe(self, days_elapsed: int) -> Optional[int]:
        """Determine which timeframe to evaluate based on days elapsed"""
        if days_elapsed >= 30:
            return 30
        elif days_elapsed >= 7:
            return 7
        elif days_elapsed >= 1:
            return 1
        else:
            return None

    def _get_no_metrics_response(self) -> Dict[str, Any]:
        """Return response when no metrics available"""
        return {
            "overall": {
                "total_signals": 0,
                "profitable_signals": 0,
                "win_rate": 0,
                "avg_return_percent": 0,
                "avg_benchmark_return_percent": 0,
                "avg_excess_return_percent": 0
            },
            "by_signal_type": {},
            "by_timeframe": {},
            "vs_benchmark": {
                "outperformed": 0,
                "underperformed": 0,
                "beat_rate": 0
            },
            "timestamp": datetime.now().isoformat(),
            "message": "No performance data available yet. Signals need time to be evaluated."
        }

    def _get_error_response(self) -> Dict[str, Any]:
        """Return error response"""
        return {
            "overall": {
                "total_signals": 0,
                "profitable_signals": 0,
                "win_rate": 0
            },
            "error": "Unable to retrieve performance metrics",
            "timestamp": datetime.now().isoformat()
        }
