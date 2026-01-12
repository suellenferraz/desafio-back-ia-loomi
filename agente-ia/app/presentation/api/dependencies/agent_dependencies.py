from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.llm.openai_client import OpenAIClient
from app.domain.services.llm_client import ILLMClient
from app.application.services.api_client import APIClient
from app.application.agents.paint_agent import PaintAgent
from app.infrastructure.config.settings import settings
from app.infrastructure.services.embedding_service import EmbeddingService
from app.domain.repositories.conversation_repository import ConversationRepository
from app.infrastructure.repositories.conversation_repository_impl import ConversationRepositoryImpl
from app.infrastructure.database.connection import get_db


def get_openai_client() -> OpenAIClient:
    return OpenAIClient()


def get_api_client() -> APIClient:
    return APIClient(base_url=settings.api.base_url)


def get_embedding_service(
    openai_client: OpenAIClient = Depends(get_openai_client)
) -> EmbeddingService:
    return EmbeddingService(embedding_client=openai_client, model=settings.openai.embedding_model)


def get_conversation_repository(db: Session = Depends(get_db)) -> ConversationRepository:
    return ConversationRepositoryImpl(db)


def get_paint_agent(
    llm_client: ILLMClient = Depends(get_openai_client),
    api_client: APIClient = Depends(get_api_client),
    embedding_service: EmbeddingService = Depends(get_embedding_service)
) -> PaintAgent:
    return PaintAgent(
        llm_client=llm_client,
        api_client=api_client,
        embedding_service=embedding_service,
        model=settings.openai.model
    )
