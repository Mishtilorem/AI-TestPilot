from ollama import AsyncClient
from app.ai.providers.base import BaseAIProvider
from app.core.config import settings


class OllamaProvider(BaseAIProvider):
    """Local AI via Ollama. Used for development."""

    def __init__(self):
        self.client = AsyncClient(host=settings.OLLAMA_BASE_URL)
        self.model = settings.OLLAMA_MODEL

    async def _chat(self, system_prompt: str, user_message: str, json_mode: bool) -> str:
        response = await self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            format="json" if json_mode else "",
        )
        return response["message"]["content"]

    async def generate(self, system_prompt: str, user_message: str) -> str:
        return await self._chat(system_prompt, user_message, json_mode=False)

    async def generate_json(self, system_prompt: str, user_message: str) -> str:
        return await self._chat(system_prompt, user_message, json_mode=True)
