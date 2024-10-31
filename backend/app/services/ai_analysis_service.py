# from langchain.chat_models import ChatOpenAI
# from langchain.chains import LLMChain
# from langchain.prompts import ChatPromptTemplate
# from datetime import datetime, timedelta
# from typing import Dict, List
# import json
# from ..config import get_settings
#
# settings = get_settings()
#
#
# class MarketAIAnalysis:
#     def __init__(self):
#         self.llm = ChatOpenAI(
#             model_name="gpt-3.5-turbo",
#             temperature=0.5,
#             api_key=settings.OPENAI_API_KEY
#         )
#         self.cache = {}
#         self.cache_duration = timedelta(hours=1)
#         self.search_tool = None
#         try:
#             from langchain_community.tools import DuckDuckGoSearchRun
#             self.search_tool = DuckDuckGoSearchRun()
#             print("DuckDuckGo search tool initialized")
#         except ImportError:
#             print("DuckDuckGo search nicht verfügbar")
#
#     def _create_analysis_prompt(self, data: Dict) -> ChatPromptTemplate:
#         system_prompt = """You are a professional market analyst. Provide a concise market
#         analysis focused on actionable insights. Focus on current conditions and avoid
#         using section headers or numerical prefixes in your response."""
#
#         user_template = """
#         Based on the market data for {symbol}:
#         Market Summary: {market_summary}
#         Recent News: {news}
#
#         Please provide:
#         - Current market sentiment and overall trend
#         - Important technical signals and their meaning
#         - Key risk factors
#         - 24-hour price outlook
#
#         Keep your response concise and actionable, avoiding section headers.
#         """
#
#         messages = [
#             ("system", system_prompt),
#             ("human", user_template)
#         ]
#         return ChatPromptTemplate.from_messages(messages)
#
#     async def get_market_news(self, symbol: str) -> List[Dict]:
#         if not self.search_tool:
#             return []
#
#         cache_key = f"news_{symbol}"
#         if cache_key in self.cache:
#             cached = self.cache[cache_key]
#             if datetime.now() - cached['timestamp'] < self.cache_duration:
#                 return cached['data']
#
#         try:
#             query = f"{symbol} stock market news last 24 hours"
#             results = self.search_tool.run(query)
#             news = []
#             for item in results.split('\n')[:3]:  # Nur die Top 3 News
#                 if item.strip():
#                     news.append({
#                         'title': item.strip(),
#                         'timestamp': datetime.now().isoformat()
#                     })
#
#             self.cache[cache_key] = {
#                 'data': news,
#                 'timestamp': datetime.now()
#             }
#             return news
#         except Exception as e:
#             print(f"News fetch error: {e}")
#             return []
#
#     def _clean_response(self, text: str) -> str:
#         """Entfernt Formatierungen und Aufzählungszeichen"""
#         lines = []
#         for line in text.split('\n'):
#             line = line.strip()
#             # Entferne numerische Präfixe und Aufzählungszeichen
#             line = line.lstrip('1234567890.-* ')
#             if line:
#                 lines.append(line)
#         return ' '.join(lines)
#
#     def _parse_response(self, response: str) -> Dict:
#         parts = response.split('\n')
#         result = {
#             'sentiment': '',
#             'technical': [],
#             'risks': [],
#             'outlook': ''
#         }
#
#         current_section = 'sentiment'
#         for part in parts:
#             part = part.strip()
#             if not part:
#                 continue
#
#             # Entferne Aufzählungszeichen und Nummerierung
#             cleaned_part = self._clean_response(part)
#
#             if 'risk' in part.lower():
#                 current_section = 'risks'
#             elif 'technical' in part.lower() or 'signal' in part.lower():
#                 current_section = 'technical'
#             elif 'outlook' in part.lower() or 'next 24' in part.lower():
#                 current_section = 'outlook'
#             else:
#                 if current_section == 'sentiment':
#                     result['sentiment'] += cleaned_part + ' '
#                 elif current_section == 'technical':
#                     result['technical'].append(cleaned_part)
#                 elif current_section == 'risks':
#                     result['risks'].append(cleaned_part)
#                 elif current_section == 'outlook':
#                     result['outlook'] += cleaned_part + ' '
#
#         return result
#
#     async def generate_market_summary(self, symbol: str, market_data: List[Dict],
#                                       technical_data: Dict, patterns: List[Dict]) -> Dict:
#         try:
#             cache_key = f"{symbol}_analysis"
#             if cache_key in self.cache:
#                 cached = self.cache[cache_key]
#                 if datetime.now() - cached['timestamp'] < self.cache_duration:
#                     return cached['data']
#
#             latest_data = market_data[-1] if market_data else {}
#             current_price = latest_data.get('close', 0)
#
#             # Vorbereitung der Analysedaten
#             market_summary = {
#                 'price': current_price,
#                 'volume': latest_data.get('volume', 0),
#                 'indicators': technical_data.get('current', {}),
#                 'patterns': [p['type'] for p in patterns]
#             }
#
#             news = await self.get_market_news(symbol)
#
#             # AI Analyse generieren
#             prompt = self._create_analysis_prompt({
#                 'symbol': symbol,
#                 'market_summary': json.dumps(market_summary, indent=2),
#                 'news': json.dumps(news, indent=2)
#             })
#
#             chain = LLMChain(llm=self.llm, prompt=prompt)
#             response = await chain.arun(
#                 symbol=symbol,
#                 market_summary=json.dumps(market_summary, indent=2),
#                 news=json.dumps(news, indent=2)
#             )
#
#             parsed = self._parse_response(response)
#             sentiment = self._determine_sentiment(market_summary)
#
#             analysis_result = {
#                 'sentiment': sentiment,
#                 'sentiment_summary': parsed['sentiment'].strip() or f"Market sentiment appears to be {sentiment}",
#                 'technical_analysis': self._format_technical_analysis(technical_data.get('current', {})),
#                 'support_resistance': {
#                     'support_levels': self._calculate_support_levels(current_price),
#                     'resistance_levels': self._calculate_resistance_levels(current_price)
#                 },
#                 'key_insights': [
#                     f"Current price: ${current_price:.2f}",
#                     *[f"{p['type']}: {p['description']}" for p in patterns],
#                     *parsed['technical']
#                 ],
#                 'risk_factors': parsed['risks'] if parsed['risks'] else
#                 self._generate_risk_factors(technical_data.get('current', {}), patterns),
#                 'short_term_outlook': parsed['outlook'].strip(),
#                 'timestamp': datetime.now().isoformat()
#             }
#
#             self.cache[cache_key] = {
#                 'data': analysis_result,
#                 'timestamp': datetime.now()
#             }
#
#             return analysis_result
#
#         except Exception as e:
#             print(f"Analysis error: {e}")
#             return {
#                 'error': str(e),
#                 'timestamp': datetime.now().isoformat()
#             }
#
#     def _determine_sentiment(self, data: Dict) -> str:
#         indicators = data.get('indicators', {})
#         rsi = indicators.get('rsi', 50)
#         macd = indicators.get('macd', 0)
#         macd_signal = indicators.get('macd_signal', 0)
#
#         if rsi > 70 or (macd > macd_signal and macd > 0):
#             return "bullish"
#         elif rsi < 30 or (macd < macd_signal and macd < 0):
#             return "bearish"
#         return "neutral"
#
#     def _calculate_support_levels(self, current_price: float) -> List[float]:
#         return [
#             round(current_price * 0.95, 2),
#             round(current_price * 0.90, 2),
#             round(current_price * 0.85, 2)
#         ]
#
#     def _calculate_resistance_levels(self, current_price: float) -> List[float]:
#         return [
#             round(current_price * 1.05, 2),
#             round(current_price * 1.10, 2),
#             round(current_price * 1.15, 2)
#         ]
#
#     def _format_technical_analysis(self, indicators: Dict) -> str:
#         return (
#             f"RSI: {indicators.get('rsi', 0):.1f}, "
#             f"MACD: {indicators.get('macd', 0):.2f}, "
#             f"Signal: {indicators.get('macd_signal', 0):.2f}"
#         )
#
#     def _generate_risk_factors(self, indicators: Dict, patterns: List[Dict]) -> List[str]:
#         risks = []
#
#         # RSI-basierte Risiken
#         rsi = indicators.get('rsi', 50)
#         if rsi > 70:
#             risks.append("Overbought conditions suggest increased downside risk")
#         elif rsi < 30:
#             risks.append("Oversold conditions indicate potential reversal")
#
#         # MACD-basierte Risiken
#         macd = indicators.get('macd', 0)
#         macd_signal = indicators.get('macd_signal', 0)
#         if macd < macd_signal:
#             risks.append("MACD below signal line indicates bearish momentum")
#
#         # Pattern-basierte Risiken
#         for pattern in patterns:
#             if 'BEARISH' in pattern['type'].upper():
#                 risks.append(f"Bearish pattern detected: {pattern['description']}")
#
#         if not risks:
#             risks.append("Market conditions appear stable")
#
#         return risks
#
#     def _format_volume(self, volume: int) -> str:
#         if volume >= 1_000_000:
#             return f"{volume / 1_000_000:.1f}M"
#         elif volume >= 1_000:
#             return f"{volume / 1_000:.1f}K"
#         return str(volume)



from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from datetime import datetime, timedelta
from typing import Dict, List
import json
from ..config import get_settings

settings = get_settings()


class MarketAIAnalysis:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.5,
            api_key=settings.OPENAI_API_KEY
        )
        # Separate Caches für News und Analysen
        self.cache = {
            'news': {},
            'analysis': {}
        }
        self.cache_duration = timedelta(hours=1)
        self.search_tool = None
        self.debug = True  # Debug-Modus standardmäßig aktiviert

        try:
            from langchain_community.tools import DuckDuckGoSearchRun
            self.search_tool = DuckDuckGoSearchRun()
            self._debug_log("DuckDuckGo search tool initialized")
        except ImportError:
            print("DuckDuckGo search nicht verfügbar")

    def _debug_log(self, message: str):
        """Debug-Logging Hilfsfunktion"""
        if self.debug:
            print(f"[AI Analysis Debug] {message}")

    def _create_analysis_prompt(self, data: Dict) -> ChatPromptTemplate:
        system_prompt = """You are a professional market analyst. Provide a concise market 
        analysis focused on actionable insights. Focus on current conditions and avoid 
        using section headers or numerical prefixes in your response."""

        user_template = """
        Based on the market data for {symbol}:
        Market Summary: {market_summary}
        Recent News: {news}

        Please provide:
        - Current market sentiment and overall trend
        - Important technical signals and their meaning
        - Key risk factors
        - 24-hour price outlook

        Keep your response concise and actionable, avoiding section headers.
        """

        messages = [
            ("system", system_prompt),
            ("human", user_template)
        ]
        return ChatPromptTemplate.from_messages(messages)

    async def get_market_news(self, symbol: str) -> List[Dict]:
        if not self.search_tool:
            return []

        cache_key = f"news_{symbol}"
        if cache_key in self.cache['news']:
            cached = self.cache['news'][cache_key]
            if datetime.now() - cached['timestamp'] < self.cache_duration:
                self._debug_log(f"Using cached news for {symbol}")
                return cached['data']

        self._debug_log(f"Fetching fresh news for {symbol}")
        try:
            query = f"{symbol} stock market news last 24 hours"
            results = self.search_tool.run(query)
            news = []
            for item in results.split('\n')[:3]:
                if item.strip():
                    news.append({
                        'title': item.strip(),
                        'timestamp': datetime.now().isoformat()
                    })

            self.cache['news'][cache_key] = {
                'data': news,
                'timestamp': datetime.now()
            }
            self._debug_log(f"Cached {len(news)} news items for {symbol}")
            return news
        except Exception as e:
            self._debug_log(f"News fetch error: {e}")
            return []

    def _clean_response(self, text: str) -> str:
        """Entfernt Formatierungen und Aufzählungszeichen"""
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            line = line.lstrip('1234567890.-* ')
            if line:
                lines.append(line)
        return ' '.join(lines)

    def _parse_response(self, response: str) -> Dict:
        parts = response.split('\n')
        result = {
            'sentiment': '',
            'technical': [],
            'risks': [],
            'outlook': ''
        }

        current_section = 'sentiment'
        for part in parts:
            part = part.strip()
            if not part:
                continue

            cleaned_part = self._clean_response(part)

            if 'risk' in part.lower():
                current_section = 'risks'
            elif 'technical' in part.lower() or 'signal' in part.lower():
                current_section = 'technical'
            elif 'outlook' in part.lower() or 'next 24' in part.lower():
                current_section = 'outlook'
            else:
                if current_section == 'sentiment':
                    result['sentiment'] += cleaned_part + ' '
                elif current_section == 'technical':
                    result['technical'].append(cleaned_part)
                elif current_section == 'risks':
                    result['risks'].append(cleaned_part)
                elif current_section == 'outlook':
                    result['outlook'] += cleaned_part + ' '

        return result

    async def generate_market_summary(self, symbol: str, market_data: List[Dict],
                                      technical_data: Dict, patterns: List[Dict]) -> Dict:
        try:
            cache_key = f"{symbol}_analysis"
            if cache_key in self.cache['analysis']:
                cached = self.cache['analysis'][cache_key]
                if datetime.now() - cached['timestamp'] < self.cache_duration:
                    self._debug_log(f"Using cached analysis for {symbol}")
                    return cached['data']

            self._debug_log(f"Generating new analysis for {symbol}")
            latest_data = market_data[-1] if market_data else {}
            current_price = latest_data.get('close', 0)

            market_summary = {
                'price': current_price,
                'volume': latest_data.get('volume', 0),
                'indicators': technical_data.get('current', {}),
                'patterns': [p['type'] for p in patterns]
            }

            self._debug_log("Fetching news for analysis")
            news = await self.get_market_news(symbol)

            self._debug_log("Calling OpenAI API for analysis")
            prompt = self._create_analysis_prompt({
                'symbol': symbol,
                'market_summary': json.dumps(market_summary, indent=2),
                'news': json.dumps(news, indent=2)
            })

            chain = LLMChain(llm=self.llm, prompt=prompt)
            response = await chain.arun(
                symbol=symbol,
                market_summary=json.dumps(market_summary, indent=2),
                news=json.dumps(news, indent=2)
            )
            self._debug_log("Received response from OpenAI")

            parsed = self._parse_response(response)
            sentiment = self._determine_sentiment(market_summary)

            analysis_result = {
                'sentiment': sentiment,
                'sentiment_summary': parsed['sentiment'].strip() or f"Market sentiment appears to be {sentiment}",
                'technical_analysis': self._format_technical_analysis(technical_data.get('current', {})),
                'support_resistance': {
                    'support_levels': self._calculate_support_levels(current_price),
                    'resistance_levels': self._calculate_resistance_levels(current_price)
                },
                'key_insights': [
                    f"Current price: ${current_price:.2f}",
                    *[f"{p['type']}: {p['description']}" for p in patterns],
                    *parsed['technical']
                ],
                'risk_factors': parsed['risks'] if parsed['risks'] else
                self._generate_risk_factors(technical_data.get('current', {}), patterns),
                'short_term_outlook': parsed['outlook'].strip(),
                'timestamp': datetime.now().isoformat()
            }

            self.cache['analysis'][cache_key] = {
                'data': analysis_result,
                'timestamp': datetime.now()
            }
            self._debug_log(f"Analysis cached for {symbol}")

            return analysis_result

        except Exception as e:
            self._debug_log(f"Analysis error: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _determine_sentiment(self, data: Dict) -> str:
        indicators = data.get('indicators', {})
        rsi = indicators.get('rsi', 50)
        macd = indicators.get('macd', 0)
        macd_signal = indicators.get('macd_signal', 0)

        if rsi > 70 or (macd > macd_signal and macd > 0):
            return "bullish"
        elif rsi < 30 or (macd < macd_signal and macd < 0):
            return "bearish"
        return "neutral"

    def _calculate_support_levels(self, current_price: float) -> List[float]:
        return [
            round(current_price * 0.95, 2),
            round(current_price * 0.90, 2),
            round(current_price * 0.85, 2)
        ]

    def _calculate_resistance_levels(self, current_price: float) -> List[float]:
        return [
            round(current_price * 1.05, 2),
            round(current_price * 1.10, 2),
            round(current_price * 1.15, 2)
        ]

    def _format_technical_analysis(self, indicators: Dict) -> str:
        return (
            f"RSI: {indicators.get('rsi', 0):.1f}, "
            f"MACD: {indicators.get('macd', 0):.2f}, "
            f"Signal: {indicators.get('macd_signal', 0):.2f}"
        )

    def _generate_risk_factors(self, indicators: Dict, patterns: List[Dict]) -> List[str]:
        risks = []

        rsi = indicators.get('rsi', 50)
        if rsi > 70:
            risks.append("Overbought conditions suggest increased downside risk")
        elif rsi < 30:
            risks.append("Oversold conditions indicate potential reversal")

        macd = indicators.get('macd', 0)
        macd_signal = indicators.get('macd_signal', 0)
        if macd < macd_signal:
            risks.append("MACD below signal line indicates bearish momentum")

        for pattern in patterns:
            if 'BEARISH' in pattern['type'].upper():
                risks.append(f"Bearish pattern detected: {pattern['description']}")

        if not risks:
            risks.append("Market conditions appear stable")

        return risks

    def _format_volume(self, volume: int) -> str:
        if volume >= 1_000_000:
            return f"{volume / 1_000_000:.1f}M"
        elif volume >= 1_000:
            return f"{volume / 1_000:.1f}K"
        return str(volume)

    def set_debug(self, enabled: bool):
        """Debug-Modus aktivieren/deaktivieren"""
        self.debug = enabled
        self._debug_log(f"Debug mode {'enabled' if enabled else 'disabled'}")