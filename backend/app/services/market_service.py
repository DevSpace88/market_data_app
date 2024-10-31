from sqlalchemy.orm import Session
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List

class MarketService:
    def __init__(self, db: Session):
        self.db = db
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)

    def _get_yf_timeframe(self, timeframe: str) -> tuple[str, str]:
        """Convert frontend timeframe to yfinance parameters"""
        timeframe_map = {
            '1D': ('1d', '5m'),
            '1W': ('7d', '15m'),
            '1M': ('1mo', '1h'),
            '3M': ('3mo', '1d'),
            '6M': ('6mo', '1d'),
            '1Y': ('1y', '1d'),
            'YTD': ('ytd', '1d'),
        }
        return timeframe_map.get(timeframe, ('1mo', '1d'))
    async def fetch_market_data(self, symbol: str, period: str = "3mo", interval: str = "1d") -> List[Dict]:
        cache_key = f"{symbol}_{period}_{interval}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if datetime.now() - cached['timestamp'] < self.cache_duration:
                return cached['data']

        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period=period, interval=interval)

            if df.empty:
                return None

            # Konvertiere zu täglichen Daten wenn nötig
            if interval != "1d" and period not in ["1d", "5d"]:
                df = df.resample('D').agg({
                    'Open': 'first',
                    'High': 'max',
                    'Low': 'min',
                    'Close': 'last',
                    'Volume': 'sum'
                }).dropna()

            data = []
            for idx, row in df.iterrows():
                data.append({
                    'timestamp': idx.isoformat(),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': int(row['Volume'])
                })

            self.cache[cache_key] = {
                'data': data,
                'timestamp': datetime.now()
            }
            return data

        except Exception as e:
            print(f"Error fetching market data: {str(e)}")
            return None

    async def detect_patterns(self, data: List[Dict]) -> List[Dict]:
        try:
            df = pd.DataFrame(data)
            df['close'] = pd.to_numeric(df['close'])
            patterns = []

            # Mehr dynamische Confidence-Berechnung
            def calculate_confidence(strength: float, volume_impact: float) -> float:
                base_confidence = min(abs(strength) * 100, 95)  # Max 95% confidence
                volume_factor = min(volume_impact * 0.2, 0.2)  # Volume kann bis zu 20% zusätzlich beisteuern
                return round(base_confidence + (base_confidence * volume_factor), 1)

            # Aktuelle Werte
            current_price = df['close'].iloc[-1]
            current_volume = df['volume'].iloc[-1]
            avg_volume = df['volume'].mean()
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1

            # Trend Stärke berechnen
            price_change = df['close'].pct_change()
            trend_strength = abs(price_change.mean()) * 100

            # Support/Resistance Levels mit dynamischer Confidence
            pivots = df['close'].rolling(window=20).std()
            recent_pivot = pivots.iloc[-1]
            price_volatility = recent_pivot / current_price

            if len(df) >= 20:
                # Support Test
                recent_lows = df['low'].rolling(window=20).min()
                if abs(current_price - recent_lows.iloc[-1]) / current_price < price_volatility:
                    strength = abs(1 - (current_price / recent_lows.iloc[-1]))
                    confidence = calculate_confidence(strength, volume_ratio)
                    patterns.append({
                        'type': 'Support',
                        'confidence': confidence,
                        'description': f'Price testing support at {recent_lows.iloc[-1]:.2f} with {confidence}% confidence'
                    })

                # Resistance Test
                recent_highs = df['high'].rolling(window=20).max()
                if abs(current_price - recent_highs.iloc[-1]) / current_price < price_volatility:
                    strength = abs(1 - (current_price / recent_highs.iloc[-1]))
                    confidence = calculate_confidence(strength, volume_ratio)
                    patterns.append({
                        'type': 'Resistance',
                        'confidence': confidence,
                        'description': f'Price testing resistance at {recent_highs.iloc[-1]:.2f} with {confidence}% confidence'
                    })

            # Trend Patterns
            if len(df) >= 5:
                recent_trend = price_change.tail(5)

                # Uptrend
                if all(recent_trend > 0):
                    confidence = calculate_confidence(trend_strength, volume_ratio)
                    patterns.append({
                        'type': 'Uptrend',
                        'confidence': confidence,
                        'description': f'Strong upward momentum with {confidence}% confidence'
                    })

                # Downtrend
                elif all(recent_trend < 0):
                    confidence = calculate_confidence(trend_strength, volume_ratio)
                    patterns.append({
                        'type': 'Downtrend',
                        'confidence': confidence,
                        'description': f'Strong downward momentum with {confidence}% confidence'
                    })

            # Breakout Detection
            if len(df) >= 20:
                upper_band = df['close'].rolling(20).mean() + (df['close'].rolling(20).std() * 2)
                lower_band = df['close'].rolling(20).mean() - (df['close'].rolling(20).std() * 2)

                if current_price > upper_band.iloc[-1]:
                    strength = (current_price - upper_band.iloc[-1]) / upper_band.iloc[-1]
                    confidence = calculate_confidence(strength, volume_ratio)
                    patterns.append({
                        'type': 'Breakout',
                        'confidence': confidence,
                        'description': f'Bullish breakout with {confidence}% confidence'
                    })

                elif current_price < lower_band.iloc[-1]:
                    strength = (lower_band.iloc[-1] - current_price) / lower_band.iloc[-1]
                    confidence = calculate_confidence(strength, volume_ratio)
                    patterns.append({
                        'type': 'Breakdown',
                        'confidence': confidence,
                        'description': f'Bearish breakdown with {confidence}% confidence'
                    })

            return patterns

        except Exception as e:
            logger.error(f"Pattern detection error: {e}")
            return []


    def generate_support_resistance_levels(self, data: List[Dict]) -> List[str]:
        try:
            df = pd.DataFrame(data)
            current_price = df['close'].iloc[-1]

            # Calculate potential levels
            pivot_high = df['high'].rolling(window=10).max().iloc[-1]
            pivot_low = df['low'].rolling(window=10).min().iloc[-1]

            # Calculate intermediate levels
            r1 = pivot_high + (pivot_high - pivot_low) * 0.382
            r2 = pivot_high + (pivot_high - pivot_low) * 0.618
            s1 = pivot_low - (pivot_high - pivot_low) * 0.382
            s2 = pivot_low - (pivot_high - pivot_low) * 0.618

            levels = [
                f"Strong resistance at ${pivot_high:.2f}",
                f"Resistance level 1 at ${r1:.2f}",
                f"Resistance level 2 at ${r2:.2f}",
                f"Current price: ${current_price:.2f}",
                f"Support level 1 at ${s1:.2f}",
                f"Support level 2 at ${s2:.2f}",
                f"Strong support at ${pivot_low:.2f}"
            ]

            return levels
        except Exception as e:
            print(f"Support/Resistance calculation error: {e}")
            return []

    def generate_short_term_outlook(self, data: List[Dict], indicators: Dict) -> str:
        try:
            current_price = data[-1]['close']
            outlook_points = []

            # RSI analysis
            if 'rsi' in indicators:
                rsi = indicators['rsi']
                if rsi > 70:
                    outlook_points.append("Overbought conditions suggest potential short-term pullback")
                elif rsi < 30:
                    outlook_points.append("Oversold conditions suggest potential short-term bounce")

            # MACD analysis
            if 'macd' in indicators and 'macd_signal' in indicators:
                if indicators['macd'] > indicators['macd_signal']:
                    outlook_points.append("MACD indicates bullish momentum")
                else:
                    outlook_points.append("MACD indicates bearish momentum")

            # Bollinger Bands analysis
            if all(k in indicators for k in ['bb_upper', 'bb_lower']):
                if current_price > indicators['bb_upper']:
                    outlook_points.append("Price above upper Bollinger Band suggests overextension")
                elif current_price < indicators['bb_lower']:
                    outlook_points.append("Price below lower Bollinger Band suggests oversold")

            # Volume analysis
            if 'volume_change' in indicators:
                if indicators['volume_change'] > 20:
                    outlook_points.append("Strong volume supports current price movement")
                elif indicators['volume_change'] < -20:
                    outlook_points.append("Declining volume suggests weakening trend")

            return " ".join(outlook_points)

        except Exception as e:
            print(f"Short-term outlook generation error: {e}")
            return "Unable to generate outlook due to insufficient data"

    # def calculate_technical_indicators(self, data: List[Dict]) -> Dict:
    #     try:
    #         df = pd.DataFrame(data)
    #         if len(df) < 2:
    #             return {}
    #
    #         df['close'] = pd.to_numeric(df['close'])
    #         indicators = {}
    #
    #         # Aktuelle (neueste) Indikatoren
    #         current = {}
    #
    #         # Moving Averages
    #         if len(df) >= 20:
    #             current['sma_20'] = float(df['close'].rolling(window=20).mean().iloc[-1])
    #         if len(df) >= 50:
    #             current['sma_50'] = float(df['close'].rolling(window=50).mean().iloc[-1])
    #
    #         # RSI
    #         if len(df) >= 14:
    #             delta = df['close'].diff()
    #             gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    #             loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    #             rs = gain / loss
    #             current['rsi'] = float(100 - (100 / (1 + rs)).iloc[-1])
    #
    #         # MACD
    #         if len(df) >= 26:
    #             exp12 = df['close'].ewm(span=12, adjust=False).mean()
    #             exp26 = df['close'].ewm(span=26, adjust=False).mean()
    #             macd = exp12 - exp26
    #             signal = macd.ewm(span=9, adjust=False).mean()
    #             current['macd'] = float(macd.iloc[-1])
    #             current['macd_signal'] = float(signal.iloc[-1])
    #
    #         # Bollinger Bands
    #         if len(df) >= 20:
    #             sma = df['close'].rolling(window=20).mean()
    #             std = df['close'].rolling(window=20).std()
    #             current['bb_upper'] = float(sma.iloc[-1] + (std.iloc[-1] * 2))
    #             current['bb_lower'] = float(sma.iloc[-1] - (std.iloc[-1] * 2))
    #             current['bb_middle'] = float(sma.iloc[-1])
    #
    #         return {
    #             'current': current,
    #             'historical': {}  # Historische Daten falls benötigt
    #         }
    #
    #     except Exception as e:
    #         print(f"Indicator calculation error: {e}")
    #         return {}

    def calculate_technical_indicators(self, data: List[Dict]) -> Dict:
        try:
            df = pd.DataFrame(data)
            if len(df) < 2:
                return {}

            df['close'] = pd.to_numeric(df['close'])
            indicators = {}
            current = {}
            historical = {'bb_upper': [], 'bb_middle': [], 'bb_lower': [], 'sma_20': [], 'sma_50': []}

            # SMA Berechnungen
            if len(df) >= 20:
                sma20 = df['close'].rolling(window=20).mean()
                current['sma_20'] = float(sma20.iloc[-1])
                historical['sma_20'] = sma20.tolist()

            if len(df) >= 50:
                sma50 = df['close'].rolling(window=50).mean()
                current['sma_50'] = float(sma50.iloc[-1])
                historical['sma_50'] = sma50.tolist()

            # Bollinger Bands
            if len(df) >= 20:
                sma = df['close'].rolling(window=20).mean()
                std = df['close'].rolling(window=20).std()

                bb_upper = sma + (std * 2)
                bb_lower = sma - (std * 2)

                current['bb_upper'] = float(bb_upper.iloc[-1])
                current['bb_middle'] = float(sma.iloc[-1])
                current['bb_lower'] = float(bb_lower.iloc[-1])

                # Historische Werte speichern
                historical['bb_upper'] = bb_upper.tolist()
                historical['bb_middle'] = sma.tolist()
                historical['bb_lower'] = bb_lower.tolist()

            # RSI
            if len(df) >= 14:
                delta = df['close'].diff()
                gain = delta.where(delta > 0, 0).rolling(window=14).mean()
                loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
                rs = gain / loss
                current['rsi'] = float(100 - (100 / (1 + rs)).iloc[-1])

            # MACD
            if len(df) >= 26:
                exp12 = df['close'].ewm(span=12, adjust=False).mean()
                exp26 = df['close'].ewm(span=26, adjust=False).mean()
                macd = exp12 - exp26
                signal = macd.ewm(span=9, adjust=False).mean()
                current['macd'] = float(macd.iloc[-1])
                current['macd_signal'] = float(signal.iloc[-1])

            return {
                'current': current,
                'historical': {
                    timestamp: {
                        indicator: values[i]
                        for indicator, values in historical.items()
                        if i < len(values) and not pd.isna(values[i])
                    }
                    for i, timestamp in enumerate(df['timestamp'])
                }
            }
        except Exception as e:
            print(f"Indicator calculation error: {e}")
            return {}

    def generate_signals(self, data: List[Dict], technical_data: Dict) -> List[Dict]:
        signals = []
        current = technical_data.get('current', {})
        latest_price = data[-1]['close'] if data else None
        timeframe_context = {
            'short': 'Short-term',
            'medium': 'Medium-term',
            'long': 'Long-term'
        }

        try:
            # RSI Signale (Kurzfristig)
            rsi = current.get('rsi')
            if rsi is not None:
                if rsi > 70:
                    signals.append({
                        'type': 'SELL',
                        'strength': 'STRONG',
                        'indicator': 'RSI',
                        'reason': f'Overbought condition (RSI: {rsi:.1f})',
                        'timeframe': 'short'
                    })
                elif rsi < 30:
                    signals.append({
                        'type': 'BUY',
                        'strength': 'STRONG',
                        'indicator': 'RSI',
                        'reason': f'Oversold condition (RSI: {rsi:.1f})',
                        'timeframe': 'short'
                    })

            # MACD Signale (Mittelfristig)
            macd = current.get('macd')
            macd_signal = current.get('macd_signal')
            if macd is not None and macd_signal is not None:
                if macd > macd_signal:
                    signals.append({
                        'type': 'BUY',
                        'strength': 'MEDIUM',
                        'indicator': 'MACD',
                        'reason': f'Bullish crossover (MACD: {macd:.2f}, Signal: {macd_signal:.2f})',
                        'timeframe': 'medium'
                    })
                elif macd < macd_signal:
                    signals.append({
                        'type': 'SELL',
                        'strength': 'MEDIUM',
                        'indicator': 'MACD',
                        'reason': f'Bearish crossover (MACD: {macd:.2f}, Signal: {macd_signal:.2f})',
                        'timeframe': 'medium'
                    })

            # Bollinger Bands Signale (Kurzfristig)
            if latest_price and all(k in current for k in ['bb_upper', 'bb_lower']):
                if latest_price > current['bb_upper']:
                    signals.append({
                        'type': 'SELL',
                        'strength': 'MEDIUM',
                        'indicator': 'Bollinger Bands',
                        'reason': f'Price above upper band (Price: {latest_price:.2f}, Upper: {current["bb_upper"]:.2f})',
                        'timeframe': 'short'
                    })
                elif latest_price < current['bb_lower']:
                    signals.append({
                        'type': 'BUY',
                        'strength': 'MEDIUM',
                        'indicator': 'Bollinger Bands',
                        'reason': f'Price below lower band (Price: {latest_price:.2f}, Lower: {current["bb_lower"]:.2f})',
                        'timeframe': 'short'
                    })

            # Moving Average Signale (Langfristig)
            if latest_price and 'sma_20' in current and 'sma_50' in current:
                if current['sma_20'] > current['sma_50']:
                    signals.append({
                        'type': 'BUY',
                        'strength': 'MEDIUM',
                        'indicator': 'Moving Averages',
                        'reason': 'Short-term MA above long-term MA (Golden Cross)',
                        'timeframe': 'long'
                    })
                elif current['sma_20'] < current['sma_50']:
                    signals.append({
                        'type': 'SELL',
                        'strength': 'MEDIUM',
                        'indicator': 'Moving Averages',
                        'reason': 'Short-term MA below long-term MA (Death Cross)',
                        'timeframe': 'long'
                    })

            # Füge Zeitrahmen-Kontext zu jedem Signal hinzu
            for signal in signals:
                signal['reason'] = f"{timeframe_context[signal['timeframe']]}: {signal['reason']}"

            return signals

        except Exception as e:
            logger.error(f"Signal generation error: {e}")
            return []
