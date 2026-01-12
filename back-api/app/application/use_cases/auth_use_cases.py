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


def update_user_admin(
    repository: UserRepository,
    user_id: int,
    username: Optional[str] = None,
    email: Optional[str] = None,
    roles: Optional[List[str]] = None
) -> Optional[User]:
    """
    Atualiza um usuário (administrativo)
    
    Args:
        repository: Repositório de usuários
        user_id: ID do usuário a ser atualizado
        username: Novo username (opcional)
        email: Novo email (opcional)
        roles: Novas roles (opcional)
    
    Returns:
        Optional[User]: Usuário atualizado ou None se não encontrado
        
    Raises:
        ValueError: Se username ou email já existirem
    """
    # Busca usuário existente
    existing_user = repository.get_by_id(user_id)
    if not existing_user:
        return None
    
    # Valida username se fornecido
    if username and username != existing_user.username:
        user_with_username = repository.get_by_username(username)
        if user_with_username and user_with_username.id != user_id:
            raise ValueError(f"Username '{username}' já está em uso")
    
    # Valida email se fornecido
    if email and email != existing_user.email:
        user_with_email = repository.get_by_email(email)
        if user_with_email and user_with_email.id != user_id:
            raise ValueError(f"Email '{email}' já está em uso")
    
    # Prepara dados para atualização
    new_username = username if username is not None else existing_user.username
    new_email = email if email is not None else existing_user.email
    new_roles = roles if roles is not None else existing_user.roles
    
    # Atualiza entidade User
    now = datetime.now(timezone.utc)
    updated_user = User(
        id=user_id,
        username=new_username,
        email=new_email,
        password_hash=existing_user.password_hash,  # Mantém senha
        roles=new_roles,
        is_active=existing_user.is_active,  # Mantém status ativo
        created_at=existing_user.created_at,
        updated_at=now
    )
    
    return repository.update(user_id, updated_user)


def delete_user_admin(repository: UserRepository, user_id: int) -> bool:
    """
    Deleta um usuário (soft delete - marca como inativo)
    
    Args:
        repository: Repositório de usuários
        user_id: ID do usuário a ser deletado
    
    Returns:
        bool: True se deletado com sucesso, False se não encontrado
    """
    return repository.delete(user_id)


def activate_user(repository: UserRepository, user_id: int) -> Optional[User]:
    """
    Ativa um usuário
    
    Args:
        repository: Repositório de usuários
        user_id: ID do usuário a ser ativado
    
    Returns:
        Optional[User]: Usuário ativado ou None se não encontrado
    """
    user = repository.get_by_id(user_id)
    if not user:
        return None
    
    if user.is_active:
        return user  # Já está ativo
    
    now = datetime.now(timezone.utc)
    updated_user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        password_hash=user.password_hash,
        roles=user.roles,
        is_active=True,
        created_at=user.created_at,
        updated_at=now
    )
    
    return repository.update(user_id, updated_user)


def deactivate_user(repository: UserRepository, user_id: int) -> Optional[User]:
    """
    Desativa um usuário
    
    Args:
        repository: Repositório de usuários
        user_id: ID do usuário a ser desativado
    
    Returns:
        Optional[User]: Usuário desativado ou None se não encontrado
    """
    user = repository.get_by_id(user_id)
    if not user:
        return None
    
    if not user.is_active:
        return user  # Já está inativo
    
    now = datetime.now(timezone.utc)
    updated_user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        password_hash=user.password_hash,
        roles=user.roles,
        is_active=False,
        created_at=user.created_at,
        updated_at=now
    )
    
    return repository.update(user_id, updated_user)


def set_user_password(repository: UserRepository, user_id: int, password: str) -> Optional[User]:
    """
    Define senha de um usuário (administrativo)
    
    Args:
        repository: Repositório de usuários
        user_id: ID do usuário
        password: Nova senha em texto plano (será hashada)
    
    Returns:
        Optional[User]: Usuário atualizado ou None se não encontrado
    """
    user = repository.get_by_id(user_id)
    if not user:
        return None
    
    # Gera hash da senha
    password_hash = AuthService.hash_password(password)
    
    now = datetime.now(timezone.utc)
    updated_user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        password_hash=password_hash,
        roles=user.roles,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=now
    )
    
    return repository.update(user_id, updated_user)


def grant_admin_role(repository: UserRepository, user_id: int) -> Optional[User]:
    """
    Concede permissão de admin a um usuário
    
    Args:
        repository: Repositório de usuários
        user_id: ID do usuário
    
    Returns:
        Optional[User]: Usuário atualizado ou None se não encontrado
    """
    user = repository.get_by_id(user_id)
    if not user:
        return None
    
    # Se já tem role admin, não faz nada
    if "admin" in user.roles:
        return user
    
    # Adiciona role admin mantendo outras roles
    new_roles = list(user.roles)
    new_roles.append("admin")
    
    now = datetime.now(timezone.utc)
    updated_user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        password_hash=user.password_hash,
        roles=new_roles,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=now
    )
    
    return repository.update(user_id, updated_user)


def revoke_admin_role(repository: UserRepository, user_id: int) -> Optional[User]:
    """
    Revoga permissão de admin de um usuário
    
    Args:
        repository: Repositório de usuários
        user_id: ID do usuário
    
    Returns:
        Optional[User]: Usuário atualizado ou None se não encontrado
        
    Raises:
        ValueError: Se tentar revogar admin de um usuário sem outras roles
    """
    user = repository.get_by_id(user_id)
    if not user:
        return None
    
    # Se não tem role admin, não faz nada
    if "admin" not in user.roles:
        return user
    
    # Remove role admin mantendo outras roles
    new_roles = [role for role in user.roles if role != "admin"]
    
    # Verifica se sobrou pelo menos uma role
    if not new_roles:
        raise ValueError("Não é possível revogar role admin: usuário deve ter pelo menos uma role")
    
    now = datetime.now(timezone.utc)
    updated_user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        password_hash=user.password_hash,
        roles=new_roles,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=now
    )
    
    return repository.update(user_id, updated_user)


def change_password(
    repository: UserRepository,
    user_id: int,
    current_password: str,
    new_password: str
) -> Optional[User]:
    """
    Altera senha do próprio usuário
    
    Args:
        repository: Repositório de usuários
        user_id: ID do usuário
        current_password: Senha atual em texto plano
        new_password: Nova senha em texto plano (será hashada)
    
    Returns:
        Optional[User]: Usuário atualizado ou None se não encontrado
        
    Raises:
        ValueError: Se senha atual inválida
    """
    user = repository.get_by_id(user_id)
    if not user:
        return None
    
    # Verifica senha atual
    if not AuthService.verify_password(current_password, user.password_hash):
        raise ValueError("Senha atual inválida")
    
    # Gera hash da nova senha
    password_hash = AuthService.hash_password(new_password)
    
    now = datetime.now(timezone.utc)
    updated_user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        password_hash=password_hash,
        roles=user.roles,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=now
    )
    
    return repository.update(user_id, updated_user)
