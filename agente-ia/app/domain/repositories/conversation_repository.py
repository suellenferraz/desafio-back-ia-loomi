from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.domain.entities.conversation import Conversation


class ConversationRepository(ABC):
    @abstractmethod
    def create(self, conversation: Conversation) -> Conversation:
        pass

    @abstractmethod
    def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: str) -> Optional[Conversation]:
        pass

    @abstractmethod
    def update(self, conversation: Conversation) -> Conversation:
        pass
