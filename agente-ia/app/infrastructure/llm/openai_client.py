from typing import List
import time
from openai import AsyncOpenAI
from app.infrastructure.config.settings import settings
from app.infrastructure.logging.logger import get_logger
from app.domain.services.llm_client import ILLMClient
from app.infrastructure.services.embedding_service import IEmbeddingClient

logger = get_logger(__name__)


class OpenAIClient(ILLMClient, IEmbeddingClient):
    def __init__(self):
        self.api_key = settings.openai.api_key
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = settings.openai.model
        self.embedding_model = settings.openai.embedding_model
        logger.info("openai_client_initialized", model=self.model, embedding_model=self.embedding_model)

    async def create_embedding(self, text: str, model: str = None) -> List[float]:
        start_time = time.time()
        model_to_use = model or self.embedding_model
        try:
            logger.debug("openai_embedding_started", model=model_to_use, text_length=len(text))
            response = await self.client.embeddings.create(
                model=model_to_use,
                input=text
            )
            embedding = response.data[0].embedding
            elapsed_time = time.time() - start_time
            logger.info(
                "openai_embedding_success",
                model=model_to_use,
                text_length=len(text),
                embedding_size=len(embedding),
                elapsed_time=round(elapsed_time, 3)
            )
            return embedding
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "openai_embedding_error",
                model=model_to_use,
                text_length=len(text),
                error=str(e),
                error_type=type(e).__name__,
                elapsed_time=round(elapsed_time, 3),
                exc_info=True
            )
            raise

    async def generate_image(self, prompt: str) -> str:
        start_time = time.time()
        try:
            logger.debug("openai_image_generation_started", prompt_preview=prompt[:50])
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            image_url = response.data[0].url
            elapsed_time = time.time() - start_time
            logger.info(
                "openai_image_generation_success",
                image_url=image_url,
                elapsed_time=round(elapsed_time, 3)
            )
            return image_url
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "openai_image_generation_error",
                prompt_preview=prompt[:50],
                error=str(e),
                error_type=type(e).__name__,
                elapsed_time=round(elapsed_time, 3),
                exc_info=True
            )
            raise
