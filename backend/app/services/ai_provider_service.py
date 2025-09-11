import os
import json
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.callbacks import CallbackManagerForLLMRun
import logging

logger = logging.getLogger(__name__)

class AIProviderService:
    def __init__(self):
        # Encryption key for API keys (in production, use environment variable)
        self.encryption_key = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
        self.cipher = Fernet(self.encryption_key)
    
    def encrypt_api_key(self, api_key: str) -> str:
        """Encrypt API key for storage"""
        if not api_key:
            return ""
        return self.cipher.encrypt(api_key.encode()).decode()
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """Decrypt API key for use"""
        if not encrypted_key:
            return ""
        try:
            return self.cipher.decrypt(encrypted_key.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to decrypt API key: {e}")
            return ""
    
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
            llm = self.get_llm(provider, model, api_key, temperature, max_tokens)
            
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
