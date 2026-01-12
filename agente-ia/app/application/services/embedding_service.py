from typing import List
import time
from app.infrastructure.llm.openai_client import OpenAIClient
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class EmbeddingService:
    def __init__(self, openai_client: OpenAIClient, model: str = "text-embedding-3-small"):
        self.openai_client = openai_client
        self.model = model
        logger.info("embedding_service_initialized", model=self.model)

    async def generate_embedding(self, text: str, model: str = None) -> List[float]:
        start_time = time.time()
        model_to_use = model or self.model
        try:
            logger.debug("embedding_service_generating", model=model_to_use, text_length=len(text))
            embedding = await self.openai_client.create_embedding(text, model=model_to_use)
            elapsed_time = time.time() - start_time
            logger.info(
                "embedding_service_success",
                model=model_to_use,
                text_length=len(text),
                embedding_size=len(embedding),
                elapsed_time=round(elapsed_time, 3)
            )
            return embedding
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "embedding_service_error",
                model=model_to_use,
                text_length=len(text),
                error=str(e),
                error_type=type(e).__name__,
                elapsed_time=round(elapsed_time, 3),
                exc_info=True
            )
            raise
