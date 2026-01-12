from typing import Optional
from datetime import datetime, timedelta, timezone
import secrets
from app.domain.entities.session import Session
from app.domain.entities.user import User
from app.domain.repositories.session_repository import SessionRepository
from app.infrastructure.config.settings import settings

def create_session(
    repository: SessionRepository,
    user: User,
    expires_delta: Optional[timedelta] = None
) -> Session:
    """
    Cria uma nova sessão para o usuário
    
    Args:
        repository: Repositório de sessões
        user: Usuário para criar a sessão
        expires_delta: Tempo de expiração (padrão: access_token_expire_minutes)
    
    Returns:
        Session: Sessão criada
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.security.access_token_expire_minutes)
    
    now = datetime.now(timezone.utc)
    expires_at = now + expires_delta
    
    # Gera session_id único
    session_id = secrets.token_urlsafe(32)
    
    session = Session(
        id=0,  # Será definido pelo banco
        user_id=user.id,
        session_id=session_id,
        expires_at=expires_at,
        created_at=now
    )
    
    return repository.create(session)


def get_session_by_id(
    repository: SessionRepository,
    session_id: str
) -> Optional[Session]:
    """
    Busca uma sessão por session_id (retorna None se expirada)
    
    Args:
        repository: Repositório de sessões
        session_id: ID da sessão
    
    Returns:
        Optional[Session]: Sessão encontrada ou None
    """
    return repository.get_by_session_id(session_id)


def get_session_by_user_id(
    repository: SessionRepository,
    user_id: int
) -> Optional[Session]:
    """
    Busca sessão ativa de um usuário
    
    Args:
        repository: Repositório de sessões
        user_id: ID do usuário
    
    Returns:
        Optional[Session]: Sessão ativa ou None
    """
    return repository.get_by_user_id(user_id)


def delete_session(
    repository: SessionRepository,
    session_id: str
) -> bool:
    """
    Deleta uma sessão por session_id (logout)
    
    Args:
        repository: Repositório de sessões
        session_id: ID da sessão
    
    Returns:
        bool: True se deletado, False se não encontrado
    """
    return repository.delete(session_id)


def delete_all_user_sessions(
    repository: SessionRepository,
    user_id: int
) -> bool:
    """
    Deleta todas as sessões de um usuário
    
    Args:
        repository: Repositório de sessões
        user_id: ID do usuário
    
    Returns:
        bool: True se deletado, False se não encontrado
    """
    return repository.delete_by_user_id(user_id)


def cleanup_expired_sessions(
    repository: SessionRepository
) -> int:
    """
    Remove todas as sessões expiradas do banco
    
    Args:
        repository: Repositório de sessões
    
    Returns:
        int: Número de sessões removidas
    """
    return repository.delete_expired()
