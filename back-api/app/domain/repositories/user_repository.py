from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.user import User

class UserRepository(ABC):
    """Interface abstrata para repositório de User"""
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Cria um novo usuário"""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Busca um usuário por ID"""
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Busca um usuário por username"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca um usuário por email"""
        pass
    
    @abstractmethod
    def update(self, user_id: int, user: User) -> Optional[User]:
        """Atualiza um usuário existente"""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Deleta um usuário (soft delete - marca como inativo)"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None) -> List[User]:
        """Lista todos os usuários com paginação e filtro opcional"""
        pass
