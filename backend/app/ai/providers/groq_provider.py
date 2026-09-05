from groq import AsyncGroq
from app.ai.providers.base import BaseAIProvider
from app.core.config import settings


class GroqProvider(BaseAIProvider):
    """Hosted AI via Groq. Used in production (Render can't run Ollama)."""

    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    async def _chat(self, system_prompt: str, user_message: str, json_mode: bool) -> str:
        kwargs = {}
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            **kwargs,
        )
        return response.choices[0].message.content or ""

    async def generate(self, system_prompt: str, user_message: str) -> str:
        return await self._chat(system_prompt, user_message, json_mode=False)

    async def generate_json(self, system_prompt: str, user_message: str) -> str:
        return await self._chat(system_prompt, user_message, json_mode=True)
