from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.conversation import Conversation
from app.domain.entities.message import Message
from app.domain.repositories.conversation_repository import ConversationRepository
from app.infrastructure.database.models.conversation_model import ConversationModel, MessageModel


class ConversationRepositoryImpl(ConversationRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, conversation: Conversation) -> Conversation:
        """Cria uma nova conversa no banco"""
        conv_model = ConversationModel(
            id=conversation.id,
            user_id=conversation.user_id,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )
        self.db.add(conv_model)
        
        # Adicionar mensagens se houver
        for msg in conversation.messages:
            msg_model = MessageModel(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at
            )
            self.db.add(msg_model)
        
        self.db.commit()
        self.db.refresh(conv_model)
        return self._model_to_entity(conv_model)

    def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """Busca conversa por ID"""
        conv_model = self.db.query(ConversationModel).filter(
            ConversationModel.id == conversation_id
        ).first()
        
        if not conv_model:
            return None
        
        return self._model_to_entity(conv_model)

    def get_by_user_id(self, user_id: str) -> Optional[Conversation]:
        """Busca última conversa do usuário"""
        conv_model = self.db.query(ConversationModel).filter(
            ConversationModel.user_id == user_id
        ).order_by(ConversationModel.created_at.desc()).first()
        
        if not conv_model:
            return None
        
        return self._model_to_entity(conv_model)

    def update(self, conversation: Conversation) -> Conversation:
        """Atualiza conversa e mensagens"""
        conv_model = self.db.query(ConversationModel).filter(
            ConversationModel.id == conversation.id
        ).first()
        
        if not conv_model:
            raise ValueError(f"Conversa {conversation.id} não encontrada")
        
        # Atualizar timestamps
        conv_model.updated_at = conversation.updated_at
        
        # Deletar mensagens antigas
        self.db.query(MessageModel).filter(
            MessageModel.conversation_id == conversation.id
        ).delete()
        
        # Adicionar novas mensagens
        for msg in conversation.messages:
            msg_model = MessageModel(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at
            )
            self.db.add(msg_model)
        
        self.db.commit()
        self.db.refresh(conv_model)
        return self._model_to_entity(conv_model)
    
    def _model_to_entity(self, model: ConversationModel) -> Conversation:
        """Converte ConversationModel para Conversation entity"""
        messages = [
            Message(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at
            )
            for msg in model.messages
        ]
        
        return Conversation(
            id=model.id,
            user_id=model.user_id,
            messages=messages,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
