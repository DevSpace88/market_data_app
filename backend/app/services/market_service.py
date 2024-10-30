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

    async def fetch_market_data(self, symbol: str, timeframe: str = "1mo") -> List[Dict]:
        cache_key = f"{symbol}_{timeframe}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if datetime.now() - cached['timestamp'] < self.cache_duration:
                return cached['data']
        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period=timeframe, interval="1d")
            if df.empty:
                return None

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
            print(f"Market data fetch error: {e}")
            return None

    def calculate_technical_indicators(self, data: List[Dict]) -> Dict:
        try:
            df = pd.DataFrame(data)
            if len(df) < 2:
                return {}

            df['close'] = pd.to_numeric(df['close'])
            indicators = {}

            # Basic price indicators
            indicators['current_price'] = float(df['close'].iloc[-1])
            indicators['price_change'] = float(df['close'].pct_change().iloc[-1] * 100)

            # Moving averages
            indicators['sma_20'] = float(df['close'].rolling(window=20).mean().iloc[-1])
            indicators['sma_50'] = float(df['close'].rolling(window=50).mean().iloc[-1])

            # RSI
            delta = df['close'].diff()
            gain = delta.where(delta > 0, 0).rolling(window=14).mean()
            loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
            rs = gain / loss
            indicators['rsi'] = float(100 - (100 / (1 + rs)).iloc[-1])

            # MACD
            exp12 = df['close'].ewm(span=12, adjust=False).mean()
            exp26 = df['close'].ewm(span=26, adjust=False).mean()
            macd = exp12 - exp26
            signal = macd.ewm(span=9, adjust=False).mean()
            indicators['macd'] = float(macd.iloc[-1])
            indicators['macd_signal'] = float(signal.iloc[-1])

            # Bollinger Bands
            sma = df['close'].rolling(window=20).mean()
            std = df['close'].rolling(window=20).std()
            indicators['bb_upper'] = float(sma.iloc[-1] + (std.iloc[-1] * 2))
            indicators['bb_lower'] = float(sma.iloc[-1] - (std.iloc[-1] * 2))
            indicators['bb_middle'] = float(sma.iloc[-1])

            # Volume indicators
            indicators['volume_sma'] = float(df['volume'].rolling(window=20).mean().iloc[-1])
            indicators['volume_change'] = float(df['volume'].pct_change().iloc[-1] * 100)

            return {k: v for k, v in indicators.items() if not pd.isna(v)}

        except Exception as e:
            print(f"Indicator calculation error: {e}")
            return {}

    async def detect_patterns(self, data: List[Dict]) -> List[Dict]:
        try:
            df = pd.DataFrame(data)
            df['close'] = pd.to_numeric(df['close'])
            patterns = []

            # Price trends
            last_close = df['close'].iloc[-1]
            last_5_closes = df['close'].tail(5)

            # Moving averages
            df['sma20'] = df['close'].rolling(window=20).mean()
            df['sma50'] = df['close'].rolling(window=50).mean()

            # Trend patterns
            if df['sma20'].iloc[-1] > df['sma50'].iloc[-1] and df['sma20'].iloc[-2] <= df['sma50'].iloc[-2]:
                patterns.append({
                    'type': 'GOLDEN_CROSS',
                    'confidence': 0.8,
                    'description': 'Bullish pattern: Short-term MA crossed above long-term MA'
                })

            # Support/Resistance levels
            rolling_high = df['high'].rolling(window=20).max()
            rolling_low = df['low'].rolling(window=20).min()

            if abs(last_close - rolling_high.iloc[-1]) / rolling_high.iloc[-1] < 0.01:
                patterns.append({
                    'type': 'RESISTANCE_TEST',
                    'confidence': 0.75,
                    'description': f'Testing resistance level at {rolling_high.iloc[-1]:.2f}'
                })

            if abs(last_close - rolling_low.iloc[-1]) / rolling_low.iloc[-1] < 0.01:
                patterns.append({
                    'type': 'SUPPORT_TEST',
                    'confidence': 0.75,
                    'description': f'Testing support level at {rolling_low.iloc[-1]:.2f}'
                })

            # Price momentum
            if all(last_5_closes.iloc[i] > last_5_closes.iloc[i - 1] for i in range(1, len(last_5_closes))):
                patterns.append({
                    'type': 'UPTREND',
                    'confidence': 0.7,
                    'description': 'Strong upward momentum detected'
                })

            return patterns

        except Exception as e:
            print(f"Pattern detection error: {e}")
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

    def generate_signals(self, data: List[Dict], indicators: Dict) -> List[Dict]:
        try:
            signals = []

            # RSI signals
            if 'rsi' in indicators:
                rsi = indicators['rsi']
                if rsi < 30:
                    signals.append({
                        'type': 'BUY',
                        'strength': 'STRONG',
                        'indicator': 'RSI',
                        'reason': f'Oversold condition (RSI: {rsi:.2f})'
                    })
                elif rsi > 70:
                    signals.append({
                        'type': 'SELL',
                        'strength': 'STRONG',
                        'indicator': 'RSI',
                        'reason': f'Overbought condition (RSI: {rsi:.2f})'
                    })

            # MACD signals
            if all(k in indicators for k in ['macd', 'macd_signal']):
                macd = indicators['macd']
                signal = indicators['macd_signal']
                if macd > signal:
                    signals.append({
                        'type': 'BUY',
                        'strength': 'MEDIUM',
                        'indicator': 'MACD',
                        'reason': f'Bullish crossover (MACD: {macd:.2f}, Signal: {signal:.2f})'
                    })
                elif macd < signal:
                    signals.append({
                        'type': 'SELL',
                        'strength': 'MEDIUM',
                        'indicator': 'MACD',
                        'reason': f'Bearish crossover (MACD: {macd:.2f}, Signal: {signal:.2f})'
                    })

            # Bollinger Bands signals
            if all(k in indicators for k in ['bb_upper', 'bb_lower']) and data:
                current_price = data[-1]['close']
                if current_price < indicators['bb_lower']:
                    signals.append({
                        'type': 'BUY',
                        'strength': 'MEDIUM',
                        'indicator': 'Bollinger Bands',
                        'reason': f'Price below lower band (Price: {current_price:.2f}, Lower: {indicators["bb_lower"]:.2f})'
                    })
                elif current_price > indicators['bb_upper']:
                    signals.append({
                        'type': 'SELL',
                        'strength': 'MEDIUM',
                        'indicator': 'Bollinger Bands',
                        'reason': f'Price above upper band (Price: {current_price:.2f}, Upper: {indicators["bb_upper"]:.2f})'
                    })

            return signals
        except Exception as e:
            print(f"Signal generation error: {e}")
            return []