from abc import ABC, abstractmethod
from typing import List


class ILLMClient(ABC):
    """Interface para cliente LLM (abstração)"""
    
    @abstractmethod
    async def create_embedding(self, text: str, model: str = None) -> List[float]:
        """Gera embedding para um texto"""
        pass
    
    @abstractmethod
    async def generate_image(self, prompt: str) -> str:
        """Gera imagem usando DALL-E"""
        pass
