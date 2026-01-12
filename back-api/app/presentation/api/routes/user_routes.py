from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.repositories.user_repository import UserRepository
from app.application.use_cases.auth_use_cases import (
    register_user as register_user_uc,
    activate_user,
    deactivate_user,
    set_user_password,
    grant_admin_role,
    revoke_admin_role,
)
from app.presentation.api.schemas.auth_schema import (
    UserCreateSchema,
    UserPasswordAdminSchema,
    UserResponseSchema,
)
from app.presentation.api.dependencies.auth_dependencies import (
    get_user_repository,
    require_roles,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreateSchema,
    repository: UserRepository = Depends(get_user_repository),
    current_user: UserResponseSchema = Depends(require_roles(["admin", "super_admin"]))
):
    """
    Cria um novo usuário (apenas admin/super_admin)
    
    Requer token JWT válido e role "admin" ou "super_admin"
    """
    try:
        user = register_user_uc(
            repository=repository,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            roles=user_data.roles
        )
        return UserResponseSchema.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[UserResponseSchema])
def list_users(
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


@router.put("/{user_id}/activation", response_model=UserResponseSchema)
def activate_user_endpoint(
    user_id: int,
    repository: UserRepository = Depends(get_user_repository),
    current_user: UserResponseSchema = Depends(require_roles(["admin", "super_admin"]))
):
    """
    Ativa um usuário (apenas admin/super_admin)
    
    Requer token JWT válido e role "admin" ou "super_admin"
    """
    user = activate_user(repository, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado"
        )
    return UserResponseSchema.model_validate(user)


@router.delete("/{user_id}/activation", response_model=UserResponseSchema)
def deactivate_user_endpoint(
    user_id: int,
    repository: UserRepository = Depends(get_user_repository),
    current_user: UserResponseSchema = Depends(require_roles(["admin", "super_admin"]))
):
    """
    Desativa um usuário (apenas admin/super_admin)
    
    Requer token JWT válido e role "admin" ou "super_admin"
    
    Validações:
    - Não permite desativar a si mesmo
    """
    # Validação: não permite desativar a si mesmo
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não é possível desativar seu próprio usuário"
        )
    
    user = deactivate_user(repository, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado"
        )
    return UserResponseSchema.model_validate(user)


@router.put("/{user_id}/password", response_model=UserResponseSchema)
def set_user_password_endpoint(
    user_id: int,
    password_data: UserPasswordAdminSchema,
    repository: UserRepository = Depends(get_user_repository),
    current_user: UserResponseSchema = Depends(require_roles(["admin", "super_admin"]))
):
    """
    Define senha de um usuário (apenas admin/super_admin)
    
    Requer token JWT válido e role "admin" ou "super_admin"
    """
    user = set_user_password(repository, user_id, password_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado"
        )
    return UserResponseSchema.model_validate(user)


@router.put("/{user_id}/roles/admin", response_model=UserResponseSchema)
def grant_admin(
    user_id: int,
    repository: UserRepository = Depends(get_user_repository),
    current_user: UserResponseSchema = Depends(require_roles(["admin", "super_admin"]))
):
    """
    Concede permissão de admin a um usuário (apenas admin/super_admin)
    
    Requer token JWT válido e role "admin" ou "super_admin"
    """
    user = grant_admin_role(repository, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado"
        )
    return UserResponseSchema.model_validate(user)


@router.delete("/{user_id}/roles/admin", response_model=UserResponseSchema)
def revoke_admin(
    user_id: int,
    repository: UserRepository = Depends(get_user_repository),
    current_user: UserResponseSchema = Depends(require_roles(["admin", "super_admin"]))
):
    """
    Revoga permissão de admin de um usuário (apenas admin/super_admin)
    
    Requer token JWT válido e role "admin" ou "super_admin"
    
    Validações:
    - Não permite revogar admin de si mesmo
    """
    # Validação: não permite revogar admin de si mesmo
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não é possível revogar permissão admin de seu próprio usuário"
        )
    
    try:
        user = revoke_admin_role(repository, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {user_id} não encontrado"
            )
        return UserResponseSchema.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
