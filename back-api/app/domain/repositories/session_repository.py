from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.session import Session

class SessionRepository(ABC):
    """Interface abstrata para repositório de Session"""
    
    @abstractmethod
    def create(self, session: Session) -> Session:
        """Cria uma nova sessão"""
        pass
    
    @abstractmethod
    def get_by_session_id(self, session_id: str) -> Optional[Session]:
        """Busca uma sessão por session_id"""
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[Session]:
        """Busca sessão ativa por user_id (última sessão)"""
        pass
    
    @abstractmethod
    def delete(self, session_id: str) -> bool:
        """Deleta uma sessão por session_id"""
        pass
    
    @abstractmethod
    def delete_by_user_id(self, user_id: int) -> bool:
        """Deleta todas as sessões de um usuário"""
        pass
    
    @abstractmethod
    def delete_expired(self) -> int:
        """Deleta todas as sessões expiradas. Retorna número de sessões deletadas"""
        pass
