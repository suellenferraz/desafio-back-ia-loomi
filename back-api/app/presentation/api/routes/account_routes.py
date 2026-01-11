from typing import Optional
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.session_repository_impl import SessionRepositoryImpl
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.session_repository import SessionRepository
from app.application.use_cases.auth_use_cases import (
    register_user as register_user_uc,
    login_user_with_session,
)
from app.application.use_cases.session_use_cases import (
    delete_session,
)
from app.infrastructure.services.auth_service import AuthService
from app.infrastructure.config.settings import settings
from app.presentation.api.schemas.auth_schema import (
    UserCreateSchema,
    UserLoginSchema,
    UserResponseSchema,
)
from app.presentation.api.dependencies.auth_dependencies import (
    get_current_user_optional,
    get_current_user_required,
    get_user_repository,
    get_session_repository,
)

router = APIRouter(prefix="/account", tags=["Account"])

@router.post("/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def signup(
    user_data: UserCreateSchema,
    request: Request,
    user_repository: UserRepository = Depends(get_user_repository),
    current_user: Optional[UserResponseSchema] = Depends(get_current_user_optional)
):
    """
    Registra um novo usuário.
    Usuário logado não pode se cadastrar até que a sessão expire ou seja encerrada.
    """
    if current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário já autenticado. Faça logout antes de registrar nova conta."
        )
    
    try:
        user = register_user_uc(
            repository=user_repository,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            roles=user_data.roles
        )
        return UserResponseSchema.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=UserResponseSchema)
def login(
    login_data: UserLoginSchema,
    request: Request,
    response: Response,
    user_repository: UserRepository = Depends(get_user_repository),
    session_repository: SessionRepository = Depends(get_session_repository),
    current_user: Optional[UserResponseSchema] = Depends(get_current_user_optional)
):
    """
    Autentica usuário, cria sessão e define JWT em cookie.
    Usuário logado não pode fazer login novamente até que a sessão expire ou seja encerrada.
    """
    if current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário já autenticado. Faça logout antes de fazer login novamente."
        )
    
    try:
        expires_delta = timedelta(minutes=settings.security.access_token_expire_minutes)
        user, session, access_token = login_user_with_session(
            user_repository=user_repository,
            session_repository=session_repository,
            username=login_data.username,
            password=login_data.password,
            expires_delta=expires_delta
        )
        
        # Define cookie httpOnly e seguro
        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=settings.security.access_token_expire_minutes * 60,
            httponly=True,
            secure=False, 
            samesite="lax",
            path="/"
        )
        
        return UserResponseSchema.model_validate(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

@router.get("/me", response_model=UserResponseSchema)
def get_current_user_info(
    current_user: UserResponseSchema = Depends(get_current_user_required)
):
    """
    Retorna informações do usuário atual autenticado.
    Renovação automática de autenticação ao acessar rotas protegidas antes da expiração.
    """
    return current_user

@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: Request,
    response: Response,
    current_user: UserResponseSchema = Depends(get_current_user_required),
    session_repository: SessionRepository = Depends(get_session_repository)
):
    """
    Faz logout do usuário ao excluir o token JWT dos cookies e remover a sessão do banco de dados.
    """
    # Obtém token do cookie ou header
    access_token = request.cookies.get("access_token")
    if not access_token:
        # Tenta obter do header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            access_token = auth_header.replace("Bearer ", "")
    
    if access_token:
        # Extrai session_id do token
        user_data = AuthService.get_user_from_token(access_token)
        if user_data and user_data.get("session_id"):
            # Deleta sessão do banco
            delete_session(session_repository, user_data["session_id"])
    
    # Remove cookie
    response.delete_cookie(
        key="access_token",
        path="/",
        samesite="lax"
    )
    
    return None
