from fastapi import Depends
from app.infrastructure.llm.openai_client import OpenAIClient
from app.application.services.api_client import APIClient
from app.application.agents.paint_agent import PaintAgent
from app.infrastructure.config.settings import settings
from app.application.services.embedding_service import EmbeddingService


def get_openai_client() -> OpenAIClient:
    return OpenAIClient()


def get_api_client() -> APIClient:
    return APIClient(base_url=settings.api.base_url)


def get_embedding_service(
    openai_client: OpenAIClient = Depends(get_openai_client)
) -> EmbeddingService:
    return EmbeddingService(openai_client=openai_client, model=settings.openai.embedding_model)


def get_paint_agent(
    openai_client: OpenAIClient = Depends(get_openai_client),
    api_client: APIClient = Depends(get_api_client),
    embedding_service: EmbeddingService = Depends(get_embedding_service)
) -> PaintAgent:
    return PaintAgent(
        openai_client=openai_client,
        api_client=api_client,
        embedding_service=embedding_service,
        model=settings.openai.model
    )
