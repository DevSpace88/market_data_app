from sqlalchemy.orm import Session
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
import logging

# Logger Konfiguration
logger = logging.getLogger(__name__)

class MarketService:
    def __init__(self, db: Session):
        self.db = db
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)

    def _get_yf_timeframe(self, timeframe: str) -> tuple[str, str]:
        """Konvertiere Frontend-Zeitrahmen zu yfinance-Parametern"""
        timeframe_map = {
            '1D': ('1d', '5m'),
            '1W': ('7d', '1h'),
            '1M': ('1mo', '1h'),
            '3M': ('3mo', '1d'),
            '6M': ('6mo', '1d'),
            '1Y': ('1y', '1d'),
            'YTD': ('ytd', '1d'),
        }
        return timeframe_map.get(timeframe, ('1mo', '1d'))

    async def fetch_market_data(self, symbol: str, period: str = "3mo", interval: str = "1d") -> List[Dict]:
        """Daten von Yahoo Finance abrufen, wenn sie nicht im Cache vorhanden sind"""
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

            data = [
                {
                    'timestamp': idx.isoformat(),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': int(row['Volume'])
                }
                for idx, row in df.iterrows()
            ]

            self.cache[cache_key] = {'data': data, 'timestamp': datetime.now()}
            return data

        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Marktdaten: {str(e)}")
            return None

    async def detect_patterns(self, data: List[Dict]) -> List[Dict]:
        """Erkennt Chart-Muster wie Doji, Hammer, Shooting Star und Engulfing Patterns"""
        try:
            if not data or len(data) < 5:
                return []

            df = pd.DataFrame(data)
            df['close'] = pd.to_numeric(df['close'])
            patterns = []

            # Definierte Muster
            def is_doji(row):
                body = abs(row['open'] - row['close'])
                total_range = row['high'] - row['low']
                return body <= 0.1 * total_range if total_range > 0 else False

            def is_hammer(row):
                body = abs(row['open'] - row['close'])
                lower_wick = min(row['open'], row['close']) - row['low']
                upper_wick = row['high'] - max(row['open'], row['close'])
                total_range = row['high'] - row['low']
                return (body < 0.3 * total_range and lower_wick > 0.6 * total_range and upper_wick < 0.1 * total_range)

            def is_shooting_star(row):
                body = abs(row['open'] - row['close'])
                lower_wick = min(row['open'], row['close']) - row['low']
                upper_wick = row['high'] - max(row['open'], row['close'])
                total_range = row['high'] - row['low']
                return (body < 0.3 * total_range and upper_wick > 0.6 * total_range and lower_wick < 0.1 * total_range)

            def is_engulfing(current, prev, bullish=True):
                if bullish:
                    return (prev['close'] < prev['open'] and current['close'] > current['open'] and
                            current['open'] < prev['close'] and current['close'] > prev['open'])
                else:
                    return (prev['close'] > prev['open'] and current['close'] < current['open'] and
                            current['open'] > prev['close'] and current['close'] < prev['open'])

            lookback = min(len(df), max(5, len(df) // 10)) # Dynamische Lookback-Periode
            for i in range(1, lookback):
                current_row = df.iloc[-i]
                prev_row = df.iloc[-i - 1] if i < len(df) - 1 else None
                timestamp = current_row['timestamp'].isoformat() if isinstance(current_row['timestamp'], pd.Timestamp) else datetime.now().isoformat()

                if is_doji(current_row):
                    patterns.append({'type': 'Doji', 'confidence': 75, 'description': 'Indecision, potential reversal', 'timestamp': timestamp})
                if prev_row is not None and is_hammer(current_row):
                    patterns.append({'type': 'Hammer', 'confidence': 80, 'description': 'Bullish reversal', 'timestamp': timestamp})
                if prev_row is not None and is_shooting_star(current_row):
                    patterns.append({'type': 'Shooting Star', 'confidence': 80, 'description': 'Bearish reversal', 'timestamp': timestamp})
                if prev_row is not None and is_engulfing(current_row, prev_row, bullish=True):
                    patterns.append({'type': 'Bullish Engulfing', 'confidence': 85, 'description': 'Strong bullish reversal', 'timestamp': timestamp})
                if prev_row is not None and is_engulfing(current_row, prev_row, bullish=False):
                    patterns.append({'type': 'Bearish Engulfing', 'confidence': 85, 'description': 'Strong bearish reversal', 'timestamp': timestamp})

            return sorted(patterns, key=lambda x: x['confidence'], reverse=True)

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

    def calculate_technical_indicators(self, data: List[Dict]) -> Dict:
        try:
            df = pd.DataFrame(data)
            if len(df) < 2:
                return {}

            df['close'] = pd.to_numeric(df['close'])
            current = {}
            historical = {}

            # Angepasste Perioden für kürzere Zeiträume
            periods = {
                'very_short': max(5, len(df) // 10),  # Sehr kurze Periode
                'short': max(10, len(df) // 5),  # Kurze Periode
                'medium': max(20, len(df) // 3),  # Mittlere Periode
                'long': max(50, len(df) // 2)  # Lange Periode
            }

            # SMA Berechnung mit angepassten Perioden
            if len(df) >= periods['medium']:
                sma_short = df['close'].rolling(window=periods['medium']).mean()
                current['sma_20'] = float(sma_short.iloc[-1])

            if len(df) >= periods['long']:
                sma_long = df['close'].rolling(window=periods['long']).mean()
                current['sma_50'] = float(sma_long.iloc[-1])

            # RSI mit angepasster Periode
            if len(df) >= periods['short']:
                delta = df['close'].diff()
                gain = delta.where(delta > 0, 0).rolling(window=periods['short']).mean()
                loss = -delta.where(delta < 0, 0).rolling(window=periods['short']).mean()
                rs = gain / loss
                current['rsi'] = float(100 - (100 / (1 + rs)).iloc[-1])

            # MACD mit angepassten Perioden
            if len(df) >= periods['long']:
                exp_short = df['close'].ewm(span=periods['short'], adjust=False).mean()
                exp_long = df['close'].ewm(span=periods['medium'], adjust=False).mean()
                macd = exp_short - exp_long
                signal = macd.ewm(span=periods['very_short'], adjust=False).mean()
                current['macd'] = float(macd.iloc[-1])
                current['macd_signal'] = float(signal.iloc[-1])

            # # Bollinger Bands mit angepasster Periode
            # if len(df) >= periods['medium']:
            #     sma = df['close'].rolling(window=periods['medium']).mean()
            #     std = df['close'].rolling(window=periods['medium']).std()
            #     current['bb_upper'] = float(sma.iloc[-1] + (std.iloc[-1] * 2))
            #     current['bb_lower'] = float(sma.iloc[-1] - (std.iloc[-1] * 2))
            #     current['bb_middle'] = float(sma.iloc[-1])
            #
            # return {
            #     'current': current,
            #     'historical': {}
            # }
            # Bollinger Bands mit historischen Daten
            if len(df) >= periods['medium']:
                sma = df['close'].rolling(window=periods['medium']).mean()
                std = df['close'].rolling(window=periods['medium']).std()

                # Current values
                current['bb_upper'] = float(sma.iloc[-1] + (std.iloc[-1] * 2))
                current['bb_lower'] = float(sma.iloc[-1] - (std.iloc[-1] * 2))
                current['bb_middle'] = float(sma.iloc[-1])

                # Historical values
                for idx, row in df.iterrows():
                    timestamp = idx.isoformat() if isinstance(idx, pd.Timestamp) else str(idx)
                    if timestamp not in historical:
                        historical[timestamp] = {}

                    i = df.index.get_loc(idx)
                    if i >= periods['medium'] - 1:
                        historical[timestamp]['bb_upper'] = float(sma.iloc[i] + (std.iloc[i] * 2))
                        historical[timestamp]['bb_lower'] = float(sma.iloc[i] - (std.iloc[i] * 2))
                        historical[timestamp]['bb_middle'] = float(sma.iloc[i])

            return {
                'current': current,
                'historical': historical
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
