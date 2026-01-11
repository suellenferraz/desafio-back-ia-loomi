from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
import bcrypt  # pyright: ignore[reportMissingImports]
from app.infrastructure.config.settings import settings
from app.domain.entities.user import User

class AuthService:
    """Serviço de autenticação e segurança"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Gera hash da senha usando bcrypt"""
        # Gera salt e hash da senha
        salt = bcrypt.gensalt()
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica se a senha em texto plano corresponde ao hash"""
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    
    @staticmethod
    def create_access_token(user: User, session_id: str, expires_delta: Optional[timedelta] = None) -> str:
        """Cria token JWT para o usuário com session_id"""
        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.security.access_token_expire_minutes)
        
        now = datetime.now(timezone.utc)
        expire = now + expires_delta
        
        # Payload do JWT (exp e iat devem ser timestamps Unix - inteiros)
        payload = {
            "sub": str(user.id),  # Subject (ID do usuário)
            "username": user.username,
            "email": user.email,
            "roles": user.roles,
            "session_id": session_id,  # ID da sessão no banco
            "exp": int(expire.timestamp()),  # Expiration time (timestamp Unix)
            "iat": int(now.timestamp()),  # Issued at (timestamp Unix)
        }
        
        # Cria o token
        encoded_jwt = jwt.encode(
            payload,
            settings.security.secret_key,
            algorithm=settings.security.algorithm
        )
        
        return encoded_jwt
    
    @staticmethod
    def decode_access_token(token: str) -> Optional[dict]:
        """Decodifica e valida o token JWT"""
        try:
            payload = jwt.decode(
                token,
                settings.security.secret_key,
                algorithms=[settings.security.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            # Token expirado
            return None
        except jwt.InvalidTokenError as e:
            # Token inválido (captura mais específica para debug)
            return None
        except Exception as e:
            # Outras exceções (para debug)
            return None
    
    @staticmethod
    def get_user_from_token(token: str) -> Optional[dict]:
        """Extrai informações do usuário do token incluindo session_id"""
        if not token:
            return None
            
        payload = AuthService.decode_access_token(token)
        if payload is None:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        return {
            "user_id": int(user_id),
            "username": payload.get("username"),
            "email": payload.get("email"),
            "roles": payload.get("roles", []),
            "session_id": payload.get("session_id"),
        }
