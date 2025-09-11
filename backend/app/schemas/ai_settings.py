from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum

class AIProvider(str, Enum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"

class AISettingsBase(BaseModel):
    ai_provider: AIProvider = Field(default=AIProvider.OPENAI, description="AI Provider")
    ai_model: str = Field(default="gpt-3.5-turbo", description="Model name")
    ai_temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature (0.0-2.0)")
    ai_max_tokens: int = Field(default=1000, ge=1, le=4000, description="Max tokens")

class AISettingsUpdate(AISettingsBase):
    ai_api_key: Optional[str] = Field(None, description="API Key (plaintext)")

class AISettingsResponse(AISettingsBase):
    """Response without sensitive API key"""
    ai_provider: str
    has_api_key: bool = Field(description="Whether user has set an API key")

class AIProviderInfo(BaseModel):
    name: str
    display_name: str
    description: str
    models: list[str]
    default_model: str
    website: str
    pricing_info: str

# Available AI Providers Configuration
AI_PROVIDERS: Dict[str, AIProviderInfo] = {
    "openai": AIProviderInfo(
        name="openai",
        display_name="OpenAI",
        description="OpenAI's GPT models including GPT-3.5 and GPT-4",
        models=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"],
        default_model="gpt-3.5-turbo",
        website="https://openai.com",
        pricing_info="Pay per token"
    ),
    "deepseek": AIProviderInfo(
        name="deepseek",
        display_name="DeepSeek",
        description="Cost-effective AI models with competitive performance",
        models=["deepseek-chat", "deepseek-coder", "deepseek-math"],
        default_model="deepseek-chat",
        website="https://deepseek.com",
        pricing_info="Very affordable pricing"
    ),
    "anthropic": AIProviderInfo(
        name="anthropic",
        display_name="Anthropic Claude",
        description="Anthropic's Claude models with strong reasoning capabilities",
        models=["claude-3-haiku", "claude-3-sonnet", "claude-3-opus"],
        default_model="claude-3-haiku",
        website="https://anthropic.com",
        pricing_info="Pay per token"
    ),
    "google": AIProviderInfo(
        name="google",
        display_name="Google Gemini",
        description="Google's Gemini models with multimodal capabilities",
        models=["gemini-pro", "gemini-pro-vision"],
        default_model="gemini-pro",
        website="https://ai.google.dev",
        pricing_info="Pay per token"
    ),
    "ollama": AIProviderInfo(
        name="ollama",
        display_name="Ollama (Local)",
        description="Run AI models locally on your machine",
        models=["llama2", "codellama", "mistral", "neural-chat"],
        default_model="llama2",
        website="https://ollama.ai",
        pricing_info="Free (local processing)"
    )
}
