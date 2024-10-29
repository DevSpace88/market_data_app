from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.tools import DuckDuckGoSearchTool
from datetime import datetime, timedelta
from typing import Dict, List
import asyncio
import json
from ..config import get_settings

settings = get_settings()


class MarketAIAnalysis:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.search_tool = DuckDuckGoSearchTool()
        self.cache = {}
        self.cache_duration = timedelta(minutes=15)

    async def get_market_news(self, symbol: str) -> List[Dict]:
        """Fetch recent market news"""
        cache_key = f"news_{symbol}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if datetime.now() - cached['timestamp'] < self.cache_duration:
                return cached['data']

        try:
            search_query = f"{symbol} stock market news analysis last 24 hours"
            results = await self.search_tool.arun(search_query)

            # Process results
            news = []
            for item in results[:5]:  # Top 5 news items
                news.append({
                    'title': item,
                    'source': 'News Search',
                    'timestamp': datetime.now().isoformat()
                })

            # Cache results
            self.cache[cache_key] = {
                'data': news,
                'timestamp': datetime.now()
            }

            return news
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def _create_analysis_prompt(self, data: Dict) -> str:
        """Create comprehensive analysis prompt"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional market analyst with expertise in 
            technical analysis, market patterns, and sentiment analysis. Analyze 
            the provided market data and provide detailed insights."""),
            ("human", """Analyze the following market data for {symbol}:

            Technical Analysis:
            {technical_data}

            Pattern Analysis:
            {patterns}

            Market News:
            {news}

            Recent Trading Activity:
            {trading_data}

            Provide a detailed analysis including:
            1. Overall market sentiment and trend direction
            2. Key technical levels and breakout points
            3. Risk assessment and market conditions
            4. Short-term outlook (24-48 hours)
            5. Notable patterns and their implications
            6. Support and resistance levels
            7. Volume analysis and significance
            8. Key events to monitor
            """)
        ])

        return prompt.format(
            symbol=data['symbol'],
            technical_data=json.dumps(data.get('technical', {}), indent=2),
            patterns=json.dumps(data.get('patterns', []), indent=2),
            news=json.dumps(data.get('news', []), indent=2),
            trading_data=json.dumps(data.get('trading', {}), indent=2)
        )

    async def generate_market_summary(self,
                                      symbol: str,
                                      market_data: List[Dict],
                                      technical_data: Dict,
                                      patterns: List[Dict]) -> Dict:
        """Generate comprehensive market analysis"""
        try:
            # Fetch news
            news = await self.get_market_news(symbol)

            # Prepare analysis data
            analysis_data = {
                'symbol': symbol,
                'technical': technical_data,
                'patterns': patterns,
                'news': news,
                'trading': {
                    'latest_price': market_data[-1]['close'] if market_data else None,
                    'volume': market_data[-1]['volume'] if market_data else None,
                    'price_change': self._calculate_price_change(market_data)
                }
            }

            # Generate prompt
            prompt = self._create_analysis_prompt(analysis_data)

            # Get AI analysis
            chain = LLMChain(llm=self.llm, prompt=prompt)
            response = await chain.arun(analysis_data)

            # Process and structure the response
            analysis = self._process_analysis_response(response)

            return {
                'summary': analysis.get('summary', ''),
                'sentiment': self._determine_sentiment(analysis),
                'technical_analysis': analysis.get('technical_analysis', ''),
                'key_insights': analysis.get('key_insights', []),
                'support_resistance': {
                    'support_levels': analysis.get('support_levels', []),
                    'resistance_levels': analysis.get('resistance_levels', [])
                },
                'risk_factors': analysis.get('risk_factors', []),
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'data_timestamp': market_data[-1]['timestamp'] if market_data else None,
                    'confidence_score': analysis.get('confidence_score', 0.0)
                }
            }

        except Exception as e:
            print(f"Error generating market summary: {e}")
            return {
                'error': 'Failed to generate market analysis',
                'timestamp': datetime.now().isoformat()
            }

    def _calculate_price_change(self, market_data: List[Dict]) -> float:
        """Calculate price change percentage"""
        if not market_data or len(market_data) < 2:
            return 0.0

        latest = market_data[-1]['close']
        previous = market_data[-2]['close']

        return ((latest - previous) / previous) * 100

    def _process_analysis_response(self, response: str) -> Dict:
        """Process and structure the AI response"""
        try:
            # Split response into sections
            sections = response.split('\n\n')

            analysis = {
                'summary': '',
                'technical_analysis': '',
                'key_insights': [],
                'support_levels': [],
                'resistance_levels': [],
                'risk_factors': [],
                'confidence_score': 0.0
            }

            current_section = 'summary'
            for section in sections:
                if 'Technical Analysis:' in section:
                    current_section = 'technical_analysis'
                    analysis[current_section] = section
                elif 'Key Insights:' in section:
                    current_section = 'key_insights'
                    insights = section.split('\n')[1:]
                    analysis[current_section] = [i.strip('- ') for i in insights if i.strip()]
                elif 'Support Levels:' in section:
                    levels = self._extract_price_levels(section)
                    analysis['support_levels'] = levels
                elif 'Resistance Levels:' in section:
                    levels = self._extract_price_levels(section)
                    analysis['resistance_levels'] = levels
                elif 'Risk Factors:' in section:
                    risks = section.split('\n')[1:]
                    analysis['risk_factors'] = [r.strip('- ') for r in risks if r.strip()]
                else:
                    if not analysis['summary']:
                        analysis['summary'] = section

            return analysis

        except Exception as e:
            print(f"Error processing analysis response: {e}")
            return {}

    def _extract_price_levels(self, text: str) -> List[float]:
        """Extract price levels from text"""
        levels = []
        try:
            for line in text.split('\n'):
                # Look for numbers in the text
                parts = line.split()
                for part in parts:
                    try:
                        level = float(part.strip('$,'))
                        levels.append(level)
                    except ValueError:
                        continue
        except Exception as e:
            print(f"Error extracting price levels: {e}")
        return sorted(levels)

    def _determine_sentiment(self, analysis: Dict) -> str:
        """Determine overall market sentiment"""
        summary = analysis.get('summary', '').lower()

        bullish_words = ['bullish', 'positive', 'upward', 'growth', 'strong']
        bearish_words = ['bearish', 'negative', 'downward', 'weak', 'decline']

        bullish_count = sum(1 for word in bullish_words if word in summary)
        bearish_count = sum(1 for word in bearish_words if word in summary)

        if bullish_count > bearish_count:
            return 'bullish'
        elif bearish_count > bullish_count:
            return 'bearish'
        return 'neutral'