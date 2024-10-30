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
        self.cache = {}
        self.cache_duration = timedelta(hours=1)
        self.search_tool = None
        try:
            from langchain_community.tools import DuckDuckGoSearchRun
            self.search_tool = DuckDuckGoSearchRun()
            print("DuckDuckGo search tool initialized")
        except ImportError:
            print("DuckDuckGo search nicht verfügbar")

    def _create_analysis_prompt(self, data: Dict) -> ChatPromptTemplate:
        system_prompt = """You are a professional market analyst. Analyze the provided 
        market data and generate insights focusing on technical analysis and market patterns."""

        user_template = """
        Analyze the following market data for {symbol}:

        Technical Analysis:
        {technical_data}

        Pattern Analysis:
        {patterns}

        News Headlines:
        {news}

        Current Trading Data:
        {trading_data}

        Provide a clear analysis covering:
        1. Overall market sentiment and trend
        2. Key support and resistance levels
        3. Technical signals and their implications
        4. Risk factors and market conditions
        5. Short-term price outlook (next 24-48h)
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
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if datetime.now() - cached['timestamp'] < self.cache_duration:
                return cached['data']

        try:
            print(f"Fetching news for {symbol}")
            query = f"{symbol} stock market news last 24 hours"
            results = self.search_tool.run(query)
            news = []
            for item in results.split('\n')[:3]:
                if item.strip():
                    news.append({
                        'title': item.strip(),
                        'timestamp': datetime.now().isoformat()
                    })

            self.cache[cache_key] = {
                'data': news,
                'timestamp': datetime.now()
            }
            return news
        except Exception as e:
            print(f"News fetch error: {e}")
            return []

    def _parse_response(self, response: str) -> Dict:
        sections = {
            'sentiment': '',
            'levels': [],
            'signals': [],
            'risks': [],
            'outlook': ''
        }

        current_section = 'sentiment'
        for line in response.split('\n'):
            line = line.strip()
            if not line:
                continue

            lower_line = line.lower()
            if 'level' in lower_line:
                current_section = 'levels'
            elif 'signal' in lower_line:
                current_section = 'signals'
            elif 'risk' in lower_line:
                current_section = 'risks'
            elif 'outlook' in lower_line:
                current_section = 'outlook'
            else:
                if isinstance(sections[current_section], list):
                    sections[current_section].append(line)
                else:
                    sections[current_section] += line + ' '

        return sections

    async def generate_market_summary(self, symbol: str, market_data: List[Dict],
                                      technical_data: Dict, patterns: List[Dict]) -> Dict:
        try:
            cache_key = f"{symbol}_analysis"
            if cache_key in self.cache:
                cached = self.cache[cache_key]
                if datetime.now() - cached['timestamp'] < self.cache_duration:
                    print(f"Using cached analysis for {symbol}")
                    return cached['data']

            news = await self.get_market_news(symbol)

            analysis_data = {
                'symbol': symbol,
                'technical_data': json.dumps(technical_data, indent=2),
                'patterns': json.dumps(patterns, indent=2),
                'news': json.dumps(news, indent=2),
                'trading_data': json.dumps({
                    'current_price': market_data[-1]['close'] if market_data else None,
                    'volume': market_data[-1]['volume'] if market_data else None,
                }, indent=2)
            }

            prompt = self._create_analysis_prompt(data=analysis_data)
            chain = LLMChain(llm=self.llm, prompt=prompt)
            response = await chain.arun(**analysis_data)

            result = self._parse_response(response)

            analysis_result = {
                'summary': result['sentiment'],
                'support_resistance': result['levels'],
                'technical_signals': result['signals'],
                'risk_factors': result['risks'],
                'short_term_outlook': result['outlook'],
                'timestamp': datetime.now().isoformat()
            }

            self.cache[cache_key] = {
                'data': analysis_result,
                'timestamp': datetime.now()
            }

            return analysis_result

        except Exception as e:
            print(f"Analysis error: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }