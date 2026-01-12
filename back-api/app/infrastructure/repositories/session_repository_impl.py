from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.sql import func
from app.domain.entities.session import Session
from app.domain.repositories.session_repository import SessionRepository
from app.infrastructure.database.models.session_model import SessionModel

class SessionRepositoryImpl(SessionRepository):
    """Implementação do repositório de Session usando SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, session: Session) -> Session:
        """Cria uma nova sessão"""
        session_model = SessionModel(
            user_id=session.user_id,
            session_id=session.session_id,
            expires_at=session.expires_at,
            created_at=session.created_at
        )
        self.db.add(session_model)
        self.db.commit()
        self.db.refresh(session_model)
        return self._model_to_entity(session_model)
    
    def get_by_session_id(self, session_id: str) -> Optional[Session]:
        """Busca uma sessão por session_id"""
        session_model = self.db.query(SessionModel).filter(
            and_(
                SessionModel.session_id == session_id,
                SessionModel.expires_at > func.timezone('UTC', func.now())
            )
        ).first()
        if session_model:
            return self._model_to_entity(session_model)
        return None
    
    def get_by_user_id(self, user_id: int) -> Optional[Session]:
        """Busca sessão ativa por user_id (última sessão não expirada)"""
        session_model = self.db.query(SessionModel).filter(
            and_(
                SessionModel.user_id == user_id,
                SessionModel.expires_at > func.timezone('UTC', func.now())
            )
        ).order_by(SessionModel.created_at.desc()).first()
        if session_model:
            return self._model_to_entity(session_model)
        return None
    
    def delete(self, session_id: str) -> bool:
        """Deleta uma sessão por session_id"""
        session_model = self.db.query(SessionModel).filter(
            SessionModel.session_id == session_id
        ).first()
        if not session_model:
            return False
        
        self.db.delete(session_model)
        self.db.commit()
        return True
    
    def delete_by_user_id(self, user_id: int) -> bool:
        """Deleta todas as sessões de um usuário"""
        sessions = self.db.query(SessionModel).filter(
            SessionModel.user_id == user_id
        ).all()
        if not sessions:
            return False
        
        for session in sessions:
            self.db.delete(session)
        self.db.commit()
        return True
    
    def delete_expired(self) -> int:
        """Deleta todas as sessões expiradas. Retorna número de sessões deletadas"""
        expired_sessions = self.db.query(SessionModel).filter(
            SessionModel.expires_at <= func.timezone('UTC', func.now())
        ).all()
        
        count = len(expired_sessions)
        for session in expired_sessions:
            self.db.delete(session)
        self.db.commit()
        return count
    
    def _model_to_entity(self, model: SessionModel) -> Session:
        """Converte SessionModel (ORM) para Session (entidade de domínio)"""
        return Session(
            id=model.id,
            user_id=model.user_id,
            session_id=model.session_id,
            expires_at=model.expires_at,
            created_at=model.created_at
        )
