from typing import Optional, List, Tuple
from datetime import datetime, timedelta, timezone
from app.domain.entities.user import User
from app.domain.entities.session import Session
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.session_repository import SessionRepository
from app.infrastructure.services.auth_service import AuthService

def register_user(
    repository: UserRepository,
    username: str,
    email: str,
    password: str,
    roles: Optional[List[str]] = None
) -> User:
    """
    Registra um novo usuário
    
    Args:
        repository: Repositório de usuários
        username: Nome de usuário
        email: Email do usuário
        password: Senha em texto plano (será hashada)
        roles: Lista de roles (padrão: ["user"])
    
    Returns:
        User: Usuário criado
        
    Raises:
        ValueError: Se username ou email já existirem, ou se houver erro de validação
    """
    # Verifica se username já existe
    existing_user = repository.get_by_username(username)
    if existing_user:
        raise ValueError(f"Username '{username}' já está em uso")
    
    # Verifica se email já existe
    existing_email = repository.get_by_email(email)
    if existing_email:
        raise ValueError(f"Email '{email}' já está em uso")
    
    # Define roles padrão se não fornecidas
    if roles is None:
        roles = ["user"]
    
    # Gera hash da senha
    password_hash = AuthService.hash_password(password)
    
    # Cria entidade User
    now = datetime.now(timezone.utc)
    user = User(
        id=0,  # Será definido pelo banco
        username=username,
        email=email,
        password_hash=password_hash,
        roles=roles,
        is_active=True,
        created_at=now,
        updated_at=now
    )
    
    # Salva no repositório
    return repository.create(user)


def login_user(
    repository: UserRepository,
    username: str,
    password: str
) -> Tuple[User, str]:
    """
    Autentica um usuário e retorna o token JWT (sem sessão)
    DEPRECATED: Use login_user_with_session ao invés disso
    
    Args:
        repository: Repositório de usuários
        username: Nome de usuário ou email
        password: Senha em texto plano
    
    Returns:
        tuple[User, str]: Tupla com (User, access_token)
        
    Raises:
        ValueError: Se credenciais inválidas ou usuário inativo
    """
    # Busca usuário por username ou email
    user = repository.get_by_username(username)
    if not user:
        user = repository.get_by_email(username)
    
    # Verifica se usuário existe
    if not user:
        raise ValueError("Credenciais inválidas")
    
    # Verifica se usuário está ativo
    if not user.is_active:
        raise ValueError("Usuário inativo")
    
    # Verifica senha
    if not AuthService.verify_password(password, user.password_hash):
        raise ValueError("Credenciais inválidas")
    
    # Gera session_id temporário (para compatibilidade)
    import secrets
    session_id = secrets.token_urlsafe(32)
    
    # Gera token JWT com session_id
    access_token = AuthService.create_access_token(user, session_id)
    
    return user, access_token


def get_user_by_id(repository: UserRepository, user_id: int) -> Optional[User]:
    """
    Busca um usuário por ID
    
    Args:
        repository: Repositório de usuários
        user_id: ID do usuário
    
    Returns:
        Optional[User]: Usuário encontrado ou None
    """
    return repository.get_by_id(user_id)


def login_user_with_session(
    user_repository: UserRepository,
    session_repository: SessionRepository,
    username: str,
    password: str,
    expires_delta: Optional[timedelta] = None
) -> Tuple[User, Session, str]:
    """
    Autentica um usuário, cria sessão e retorna token JWT
    
    Args:
        user_repository: Repositório de usuários
        session_repository: Repositório de sessões
        username: Nome de usuário ou email
        password: Senha em texto plano
        expires_delta: Tempo de expiração da sessão
    
    Returns:
        Tuple[User, Session, str]: (User, Session, access_token)
        
    Raises:
        ValueError: Se credenciais inválidas ou usuário inativo
    """
    # Busca usuário por username ou email
    user = user_repository.get_by_username(username)
    if not user:
        user = user_repository.get_by_email(username)
    
    # Verifica se usuário existe
    if not user:
        raise ValueError("Credenciais inválidas")
    
    # Verifica se usuário está ativo
    if not user.is_active:
        raise ValueError("Usuário inativo")
    
    # Verifica senha
    if not AuthService.verify_password(password, user.password_hash):
        raise ValueError("Credenciais inválidas")
    
    # Deleta sessões antigas do usuário (opcional - pode manter múltiplas)
    # session_repository.delete_by_user_id(user.id)
    
    # Cria nova sessão
    from app.application.use_cases.session_use_cases import create_session
    session = create_session(session_repository, user, expires_delta)
    
    # Gera token JWT com session_id
    access_token = AuthService.create_access_token(user, session.session_id, expires_delta)
    
    return user, session, access_token


def get_user_by_token(
    repository: UserRepository,
    session_repository: SessionRepository,
    token: str
) -> User:
    """
    Busca um usuário a partir de um token JWT validando sessão
    
    Args:
        repository: Repositório de usuários
        session_repository: Repositório de sessões
        token: Token JWT
    
    Returns:
        User: Usuário encontrado
        
    Raises:
        ValueError: Se token inválido, expirado ou sessão inválida
    """
    # Decodifica token
    user_data = AuthService.get_user_from_token(token)
    if not user_data:
        raise ValueError("Token inválido ou expirado")
    
    session_id = user_data.get("session_id")
    if not session_id:
        raise ValueError("Token não contém session_id")
    
    # Valida sessão no banco
    from app.application.use_cases.session_use_cases import get_session_by_id
    session = get_session_by_id(session_repository, session_id)
    if not session:
        raise ValueError("Sessão inválida ou expirada")
    
    # Busca usuário
    user = repository.get_by_id(user_data["user_id"])
    if not user:
        raise ValueError("Usuário não encontrado")
    
    # Verifica se usuário está ativo
    if not user.is_active:
        raise ValueError("Usuário inativo")
    
    # Verifica se user_id da sessão corresponde ao user_id do token
    if session.user_id != user.id:
        raise ValueError("Sessão inválida")
    
    return user
