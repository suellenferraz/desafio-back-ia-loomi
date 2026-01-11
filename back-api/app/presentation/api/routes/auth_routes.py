from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.domain.repositories.user_repository import UserRepository
from app.presentation.api.schemas.auth_schema import UserResponseSchema
from app.presentation.api.dependencies.auth_dependencies import require_roles

router = APIRouter(prefix="/auth", tags=["RBAC"])

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Dependency injection para obter repositório de User"""
    return UserRepositoryImpl(db)

@router.get("/admin/users", response_model=List[UserResponseSchema])
def list_all_users(
    skip: int = 0,
    limit: int = 100,
    repository: UserRepository = Depends(get_user_repository),
    current_user: UserResponseSchema = Depends(require_roles(["admin", "super_admin"]))
):
    """
    Lista todos os usuários (apenas admin/super_admin)
    
    - **skip**: Número de registros para pular
    - **limit**: Número máximo de registros
    
    Requer token JWT válido e role "admin" ou "super_admin"
    """
    users = repository.get_all(skip=skip, limit=limit)
    return [UserResponseSchema.model_validate(user) for user in users]
