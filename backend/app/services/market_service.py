import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pandas_ta as ta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from ..models.database import MarketData, TechnicalIndicator, PatternDetection
from ..config import get_settings

settings = get_settings()


class MarketService:
    def __init__(self, db: Session):
        self.db = db
        self.cache = {}
        self.cache_duration = timedelta(seconds=settings.CACHE_DURATION)

    def _get_cache_key(self, symbol: str, timeframe: str) -> str:
        return f"{symbol}_{timeframe}"

    def _is_cache_valid(self, cache_key: str) -> bool:
        if cache_key not in self.cache:
            return False
        return (datetime.now() - self.cache[cache_key]['timestamp']) < self.cache_duration

    async def fetch_market_data(self, symbol: str, timeframe: str = "1d") -> Dict:
        """Fetch market data with caching"""
        cache_key = self._get_cache_key(symbol, timeframe)

        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']

        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period=timeframe)

            # Convert to list of records
            data = []
            for idx, row in df.iterrows():
                record = {
                    'timestamp': idx.isoformat(),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': int(row['Volume'])
                }
                data.append(record)

                # Save to database
                db_record = MarketData(
                    symbol=symbol,
                    timestamp=idx,
                    open_price=row['Open'],
                    high_price=row['High'],
                    low_price=row['Low'],
                    close_price=row['Close'],
                    volume=row['Volume']
                )
                self.db.add(db_record)

            self.db.commit()

            # Update cache
            self.cache[cache_key] = {
                'data': data,
                'timestamp': datetime.now()
            }

            return data
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return None

    def calculate_technical_indicators(self, data: List[Dict]) -> Dict:
        """Calculate technical indicators from market data"""
        try:
            # Convert to DataFrame
            df = pd.DataFrame(data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)

            # Calculate indicators
            indicators = {}

            # Trend
            indicators['sma_20'] = ta.sma(df['close'], length=20).iloc[-1]
            indicators['sma_50'] = ta.sma(df['close'], length=50).iloc[-1]
            indicators['ema_20'] = ta.ema(df['close'], length=20).iloc[-1]

            # Momentum
            indicators['rsi'] = ta.rsi(df['close'], length=14).iloc[-1]
            macd = ta.macd(df['close'])
            indicators['macd'] = macd['MACD_12_26_9'].iloc[-1]
            indicators['macd_signal'] = macd['MACDs_12_26_9'].iloc[-1]

            # Volatility
            bb = ta.bbands(df['close'])
            indicators['bb_upper'] = bb['BBU_20_2.0'].iloc[-1]
            indicators['bb_lower'] = bb['BBL_20_2.0'].iloc[-1]
            indicators['bb_middle'] = bb['BBM_20_2.0'].iloc[-1]

            # Store in database
            for name, value in indicators.items():
                if pd.notnull(value):
                    record = TechnicalIndicator(
                        market_data_id=data[-1]['timestamp'],
                        indicator_type=name,
                        value=float(value),
                        timestamp=datetime.now()
                    )
                    self.db.add(record)

            self.db.commit()

            return indicators
        except Exception as e:
            print(f"Error calculating indicators: {e}")
            return {}

    async def detect_patterns(self, data: List[Dict]) -> List[Dict]:
        """Detect technical patterns in market data"""
        try:
            df = pd.DataFrame(data)
            patterns = []

            # Trend patterns
            if len(df) >= 50:
                sma20 = ta.sma(df['close'], length=20)
                sma50 = ta.sma(df['close'], length=50)

                if (sma20.iloc[-1] > sma50.iloc[-1] and
                        sma20.iloc[-2] <= sma50.iloc[-2]):
                    patterns.append({
                        'type': 'GOLDEN_CROSS',
                        'confidence': 0.8,
                        'description': 'Potential bullish trend reversal'
                    })
                elif (sma20.iloc[-1] < sma50.iloc[-1] and
                      sma20.iloc[-2] >= sma50.iloc[-2]):
                    patterns.append({
                        'type': 'DEATH_CROSS',
                        'confidence': 0.8,
                        'description': 'Potential bearish trend reversal'
                    })

            # Support/Resistance
            last_price = df['close'].iloc[-1]
            resistance = df['high'].rolling(20).max().iloc[-1]
            support = df['low'].rolling(20).min().iloc[-1]

            if abs(last_price - resistance) / resistance < 0.01:
                patterns.append({
                    'type': 'RESISTANCE_TEST',
                    'confidence': 0.7,
                    'description': f'Price testing resistance at {resistance:.2f}'
                })

            if abs(last_price - support) / support < 0.01:
                patterns.append({
                    'type': 'SUPPORT_TEST',
                    'confidence': 0.7,
                    'description': f'Price testing support at {support:.2f}'
                })

            # Store patterns
            for pattern in patterns:
                record = PatternDetection(
                    symbol=data[0]['symbol'],
                    pattern_type=pattern['type'],
                    confidence=pattern['confidence'],
                    description=pattern['description']
                )
                self.db.add(record)

            self.db.commit()

            return patterns
        except Exception as e:
            print(f"Error detecting patterns: {e}")
            return []

    def generate_signals(self, data: List[Dict], indicators: Dict) -> List[Dict]:
        """Generate trading signals"""
        signals = []
        try:
            # RSI signals
            if indicators.get('rsi'):
                rsi = indicators['rsi']
                if rsi < 30:
                    signals.append({
                        'type': 'BUY',
                        'strength': 'STRONG',
                        'indicator': 'RSI',
                        'reason': 'Oversold condition'
                    })
                elif rsi > 70:
                    signals.append({
                        'type': 'SELL',
                        'strength': 'STRONG',
                        'indicator': 'RSI',
                        'reason': 'Overbought condition'
                    })

            # MACD signals
            if all(k in indicators for k in ['macd', 'macd_signal']):
                if (indicators['macd'] > indicators['macd_signal']):
                    signals.append({
                        'type': 'BUY',
                        'strength': 'MEDIUM',
                        'indicator': 'MACD',
                        'reason': 'Bullish crossover'
                    })
                elif (indicators['macd'] < indicators['macd_signal']):
                    signals.append({
                        'type': 'SELL',
                        'strength': 'MEDIUM',
                        'indicator': 'MACD',
                        'reason': 'Bearish crossover'
                    })

            # Bollinger Bands signals
            last_close = data[-1]['close']
            if all(k in indicators for k in ['bb_upper', 'bb_lower']):
                if last_close < indicators['bb_lower']:
                    signals.append({
                        'type': 'BUY',
                        'strength': 'MEDIUM',
                        'indicator': 'BB',
                        'reason': 'Price below lower band'
                    })
                elif last_close > indicators['bb_upper']:
                    signals.append({
                        'type': 'SELL',
                        'strength': 'MEDIUM',
                        'indicator': 'BB',
                        'reason': 'Price above upper band'
                    })

            return signals
        except Exception as e:
            print(f"Error generating signals: {e}")
            return []