from typing import Optional, List, Callable
from fastapi import Request, Depends, HTTPException, status, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.session_repository_impl import SessionRepositoryImpl
from app.infrastructure.repositories.paint_repository_impl import PaintRepositoryImpl
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.session_repository import SessionRepository
from app.domain.repositories.paint_repository import PaintRepository
from app.application.use_cases.auth_use_cases import get_user_by_token
from app.presentation.api.schemas.auth_schema import UserResponseSchema
from app.infrastructure.config.settings import settings

security = HTTPBearer(auto_error=False)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Dependency injection para obter repositório de User"""
    return UserRepositoryImpl(db)

def get_session_repository(db: Session = Depends(get_db)) -> SessionRepository:
    """Dependency injection para obter repositório de Session"""
    return SessionRepositoryImpl(db)

def get_paint_repository(db: Session = Depends(get_db)) -> PaintRepository:
    """Dependency injection para obter repositório de Paint"""
    return PaintRepositoryImpl(db)

def get_current_user_optional(
    request: Request,
    access_token: Optional[str] = Cookie(None, alias="access_token"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    user_repository: UserRepository = Depends(get_user_repository),
    session_repository: SessionRepository = Depends(get_session_repository)
) -> Optional[UserResponseSchema]:
    """
    Obtém usuário atual de cookie ou header Authorization (opcional)
    Retorna None se não autenticado (não levanta exceção)
    """
    token = None
    
    # Tenta obter token do cookie primeiro
    if access_token:
        token = access_token
    # Se não tem cookie, tenta header Authorization
    elif credentials and credentials.credentials:
        token = credentials.credentials
    
    if not token:
        return None
    
    try:
        user = get_user_by_token(
            repository=user_repository,
            session_repository=session_repository,
            token=token
        )
        return UserResponseSchema.model_validate(user)
    except ValueError:
        return None

def get_current_user_required(
    request: Request,
    access_token: Optional[str] = Cookie(None, alias="access_token"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    user_repository: UserRepository = Depends(get_user_repository),
    session_repository: SessionRepository = Depends(get_session_repository)
) -> UserResponseSchema:
    """
    Obtém usuário atual de cookie ou header Authorization (obrigatório)
    Levanta exceção 401 se não autenticado
    """
    token = None
    
    # Tenta obter token do cookie primeiro
    if access_token:
        token = access_token
    # Se não tem cookie, tenta header Authorization
    elif credentials and credentials.credentials:
        token = credentials.credentials
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user = get_user_by_token(
            repository=user_repository,
            session_repository=session_repository,
            token=token
        )
        return UserResponseSchema.model_validate(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_roles(allowed_roles: List[str]) -> Callable:
    """
    Factory function que retorna uma dependência para verificar roles do usuário (RBAC)
    Usa o novo sistema de autenticação com sessões
    
    Args:
        allowed_roles: Lista de roles permitidas (ex: ["admin"], ["admin", "super_admin"])
    
    Returns:
        Dependency function que verifica se o usuário tem uma das roles permitidas
        
    Example:
        @router.get("/admin-only")
        def admin_endpoint(user: UserResponseSchema = Depends(require_roles(["admin"]))):
            ...
    """
    def role_checker(current_user: UserResponseSchema = Depends(get_current_user_required)) -> UserResponseSchema:
        """
        Verifica se o usuário atual tem uma das roles permitidas
        """
        user_roles = set(current_user.roles)
        allowed_set = set(allowed_roles)
        
        # Verifica se há interseção entre as roles do usuário e as permitidas
        if not user_roles.intersection(allowed_set):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Roles necessárias: {allowed_roles}. Suas roles: {current_user.roles}",
            )
        
        return current_user
    
    return role_checker
