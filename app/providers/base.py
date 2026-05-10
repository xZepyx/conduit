from abc import ABC, abstractmethod
from typing import AsyncGenerator


class BaseProvider(ABC):
    """Base class for LLM providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    async def stream_chat(
        self, model: str, messages: list
    ) -> AsyncGenerator[dict, None]:
        """Stream chat completion. Yields dicts:
        - {"content": "text"} for content deltas
        - {"done": True} for the final done signal
        - {"error": "message"} for errors
        """
        ...

    @abstractmethod
    async def chat(self, model: str, messages: list) -> str:
        """Non-streaming chat completion, returns the full response content."""
        ...
