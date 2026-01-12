from typing import Optional
from uuid import UUID
from app.domain.entities.conversation import Conversation
from app.domain.repositories.conversation_repository import ConversationRepository


class ConversationRepositoryImpl(ConversationRepository):
    def __init__(self):
        self._conversations = {}

    def create(self, conversation: Conversation) -> Conversation:
        self._conversations[str(conversation.id)] = conversation
        return conversation

    def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        return self._conversations.get(str(conversation_id))

    def get_by_user_id(self, user_id: str) -> Optional[Conversation]:
        for conv in self._conversations.values():
            if conv.user_id == user_id:
                return conv
        return None

    def update(self, conversation: Conversation) -> Conversation:
        self._conversations[str(conversation.id)] = conversation
        return conversation
