from functools import lru_cache
from app.core.config import settings
from app.ai.providers.base import BaseAIProvider


@lru_cache
def get_ai_provider() -> BaseAIProvider:
    """Return the configured AI provider. Swap providers via the AI_PROVIDER env var."""
    if settings.AI_PROVIDER == "groq":
        from app.ai.providers.groq_provider import GroqProvider

        return GroqProvider()
    from app.ai.providers.ollama_provider import OllamaProvider

    return OllamaProvider()
