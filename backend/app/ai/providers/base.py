from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    """Common interface every AI provider implements.

    Adding a new provider (OpenAI, Gemini, etc.) means writing one subclass
    and registering it in the factory — nothing else in the app changes.
    """

    @abstractmethod
    async def generate(self, system_prompt: str, user_message: str) -> str:
        """Return the model's text response. Used for free-form output."""

    @abstractmethod
    async def generate_json(self, system_prompt: str, user_message: str) -> str:
        """Return a response constrained to valid JSON (provider JSON mode)."""
