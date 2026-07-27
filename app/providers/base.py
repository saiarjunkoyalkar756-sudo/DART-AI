# app/providers/base.py — Abstract LLM Provider Base Class
from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Dict, Any

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_stream(
        self, 
        model_id: str, 
        messages: List[Dict[str, Any]], 
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Yields SSE tokens asynchronously from provider."""
        pass
