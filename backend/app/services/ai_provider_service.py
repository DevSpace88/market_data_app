from typing import Optional, Dict, Any, List
import json
import time
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, SystemMessage
import logging

logger = logging.getLogger(__name__)

class AIProviderService:
    def __init__(self):
        # No encryption for API keys; keys are stored in plaintext as requested
        # Simple in-memory cache for structured analyses
        self._analysis_cache: Dict[str, Dict[str, Any]] = {}
        self._analysis_cache_ts: Dict[str, float] = {}
        self._analysis_cache_ttl_seconds: int = 60 * 60 * 24  # 24 hours
    
    def get_llm(self, provider: str, model: str, api_key: str, temperature: float = 0.7, max_tokens: int = 1000):
        """Get configured LLM instance based on provider"""
        try:
            if provider == "openai":
                return ChatOpenAI(
                    model=model,
                    openai_api_key=api_key,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            elif provider == "deepseek":
                # DeepSeek uses OpenAI-compatible API
                return ChatOpenAI(
                    model=model,
                    openai_api_key=api_key,
                    openai_api_base="https://api.deepseek.com/v1",
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            elif provider == "anthropic":
                return ChatAnthropic(
                    model=model,
                    anthropic_api_key=api_key,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            elif provider == "google":
                return ChatGoogleGenerativeAI(
                    model=model,
                    google_api_key=api_key,
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            elif provider == "ollama":
                return Ollama(
                    model=model,
                    base_url="http://localhost:11434",  # Default Ollama URL
                    temperature=temperature,
                    num_predict=max_tokens
                )
            else:
                raise ValueError(f"Unsupported AI provider: {provider}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM for provider {provider}: {e}")
            raise
    
    async def analyze_market_data(self, symbol: str, market_data: Dict[str, Any], 
                                provider: str, model: str, api_key: str, 
                                temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Analyze market data using specified AI provider"""
        try:
            llm = self.get_llm(provider, model, api_key, temperature=temperature, max_tokens=max_tokens)
            
            # Prepare market data context
            context = f"""
            Symbol: {symbol}
            Current Price: ${market_data.get('price', 'N/A')}
            Change: {market_data.get('change', 'N/A')} ({market_data.get('change_percent', 'N/A')}%)
            Volume: {market_data.get('volume', 'N/A'):,}
            Market Cap: ${market_data.get('market_cap', 'N/A'):,}
            P/E Ratio: {market_data.get('pe_ratio', 'N/A')}
            """
            
            if 'chart_data' in market_data:
                chart_trend = "rising" if market_data['chart_data'][-1] > market_data['chart_data'][0] else "falling"
                context += f"\nChart Trend: {chart_trend}"
            
            # Create analysis prompt
            system_prompt = """You are a professional financial analyst. Analyze the provided market data and give a concise, actionable analysis. Focus on:
            1. Key trends and patterns
            2. Technical indicators
            3. Risk assessment
            4. Investment recommendation (buy/hold/sell)
            
            Keep the analysis under 200 words and use professional financial terminology."""
            
            human_prompt = f"Please analyze this market data:\n\n{context}"
            
            # Generate analysis
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            response = await llm.ainvoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"AI analysis failed for {symbol}: {e}")
            return f"Analysis temporarily unavailable. Error: {str(e)}"

    async def generate_structured_market_analysis(
        self,
        symbol: str,
        market_data: Dict[str, Any],
        technical_indicators: Dict[str, Any],
        patterns: List[Dict[str, Any]],
        provider: str,
        model: str,
        api_key: str,
        timeframe: str = "1M",
        temperature: float = 0.7,
        max_tokens: int = 800,
    ) -> Dict[str, Any]:
        """Generate a structured market analysis object expected by the frontend.

        Returns keys:
        - sentiment (bullish|bearish|neutral)
        - sentiment_summary (str)
        - technical_analysis (str)
        - support_resistance { support_levels: number[], resistance_levels: number[] }
        - key_insights: str[]
        - risk_factors: str[]
        - short_term_outlook: str
        - timestamp: ISO string
        """
        try:
            # Cache key includes provider/model/symbol/timeframe to avoid cross-mixing
            cache_key = f"{provider}:{model}:{symbol}:{timeframe}"
            now = time.time()
            if cache_key in self._analysis_cache:
                ts = self._analysis_cache_ts.get(cache_key, 0)
                if now - ts < self._analysis_cache_ttl_seconds:
                    return self._analysis_cache[cache_key]

            llm = self.get_llm(provider, model, api_key, temperature=temperature, max_tokens=max_tokens)

            # Prepare structured prompt
            context = {
                "symbol": symbol,
                "current_price": market_data.get("price"),
                "price_change": market_data.get("change_percent"),
                "volume": market_data.get("volume"),
                "market_cap": market_data.get("market_cap"),
                "pe_ratio": market_data.get("pe_ratio"),
                "technical_indicators": technical_indicators,
                "patterns": patterns,
            }

            system_prompt = (
                "You are a professional financial analyst. Respond ONLY with strict JSON matching the schema. "
                "Do not include markdown or extra commentary."
            )

            schema_description = (
                "{\n"
                "  \"sentiment\": \"bullish|bearish|neutral\",\n"
                "  \"sentiment_summary\": string,\n"
                "  \"technical_analysis\": string,\n"
                "  \"support_resistance\": {\n"
                "    \"support_levels\": number[],\n"
                "    \"resistance_levels\": number[]\n"
                "  },\n"
                "  \"key_insights\": string[],\n"
                "  \"risk_factors\": string[],\n"
                "  \"short_term_outlook\": string\n"
                "}"
            )

            human_prompt = (
                "Using the following market context, produce JSON exactly matching the schema: "
                f"\nSchema: {schema_description}\n\n"
                f"Context JSON:\n{json.dumps(context, default=str)}\n"
            )

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt),
            ]

            response = await llm.ainvoke(messages)
            raw = response.content if hasattr(response, "content") else str(response)

            try:
                parsed = json.loads(raw)
            except Exception:
                # Attempt to extract JSON substring if model wrapped in text
                start = raw.find("{")
                end = raw.rfind("}")
                if start != -1 and end != -1 and end > start:
                    try:
                        parsed = json.loads(raw[start : end + 1])
                    except Exception:
                        parsed = {}
                else:
                    parsed = {}

            # Fallbacks and normalization
            sentiment = str(parsed.get("sentiment", "neutral")).lower()
            if sentiment not in {"bullish", "bearish", "neutral"}:
                sentiment = "neutral"

            support_levels = parsed.get("support_resistance", {}).get("support_levels") or []
            resistance_levels = parsed.get("support_resistance", {}).get("resistance_levels") or []

            # If model didn't provide levels, approximate from price
            price = market_data.get("price") or 0
            if not support_levels and isinstance(price, (int, float)) and price:
                support_levels = [round(price * 0.97, 2), round(price * 0.94, 2), round(price * 0.9, 2)]
            if not resistance_levels and isinstance(price, (int, float)) and price:
                resistance_levels = [round(price * 1.03, 2), round(price * 1.06, 2), round(price * 1.1, 2)]

            result: Dict[str, Any] = {
                "sentiment": sentiment,
                "sentiment_summary": parsed.get("sentiment_summary") or "",
                "technical_analysis": parsed.get("technical_analysis") or "",
                "support_resistance": {
                    "support_levels": support_levels,
                    "resistance_levels": resistance_levels,
                },
                "key_insights": parsed.get("key_insights") or [],
                "risk_factors": parsed.get("risk_factors") or [],
                "short_term_outlook": parsed.get("short_term_outlook") or "",
            }

            # Store in cache
            self._analysis_cache[cache_key] = result
            self._analysis_cache_ts[cache_key] = now
            return result
        except Exception as e:
            logger.error(f"Structured AI analysis failed for {symbol}: {e}")
            # Conservative fallback with minimal info
            price = market_data.get("price") or 0
            return {
                "sentiment": "neutral",
                "sentiment_summary": "",
                "technical_analysis": "",
                "support_resistance": {
                    "support_levels": [round(price * 0.97, 2), round(price * 0.94, 2), round(price * 0.9, 2)] if price else [],
                    "resistance_levels": [round(price * 1.03, 2), round(price * 1.06, 2), round(price * 1.1, 2)] if price else [],
                },
                "key_insights": [],
                "risk_factors": [],
                "short_term_outlook": "",
            }
    
    def test_api_connection(self, provider: str, model: str, api_key: str) -> Dict[str, Any]:
        """Test API connection for a provider"""
        try:
            llm = self.get_llm(provider, model, api_key, temperature=0.1, max_tokens=50)
            
            # Simple test message
            test_message = HumanMessage(content="Hello, please respond with 'Connection successful'")
            response = llm.invoke([test_message])
            
            return {
                "success": True,
                "message": "Connection successful",
                "response": response.content[:100] if hasattr(response, 'content') else str(response)
            }
        except Exception as e:
            logger.error(f"API connection test failed for {provider}: {e}")
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}",
                "error": str(e)
            }

# Global instance
ai_provider_service = AIProviderService()
