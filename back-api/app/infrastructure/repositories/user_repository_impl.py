from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models.user_model import UserModel

class UserRepositoryImpl(UserRepository):
    """Implementação do repositório de User usando SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user: User) -> User:
        """Cria um novo usuário"""
        user_model = UserModel(
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            roles=user.roles,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)
        return self._model_to_entity(user_model)
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Busca um usuário por ID"""
        user_model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_model:
            return self._model_to_entity(user_model)
        return None
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Busca um usuário por username"""
        user_model = self.db.query(UserModel).filter(UserModel.username == username).first()
        if user_model:
            return self._model_to_entity(user_model)
        return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca um usuário por email"""
        user_model = self.db.query(UserModel).filter(UserModel.email == email).first()
        if user_model:
            return self._model_to_entity(user_model)
        return None
    
    def update(self, user_id: int, user: User) -> Optional[User]:
        """Atualiza um usuário existente"""
        user_model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            return None
        
        user_model.username = user.username
        user_model.email = user.email
        user_model.password_hash = user.password_hash
        user_model.roles = user.roles
        user_model.is_active = user.is_active
        user_model.updated_at = user.updated_at
        
        self.db.commit()
        self.db.refresh(user_model)
        return self._model_to_entity(user_model)
    
    def delete(self, user_id: int) -> bool:
        """Deleta um usuário (soft delete - marca como inativo)"""
        user_model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            return False
        
        # Soft delete: marca como inativo ao invés de deletar fisicamente
        user_model.is_active = False
        self.db.commit()
        return True
    
    def get_all(self, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None) -> List[User]:
        """Lista todos os usuários com paginação e filtro opcional"""
        query = self.db.query(UserModel)
        
        if is_active is not None:
            query = query.filter(UserModel.is_active == is_active)
        
        user_models = query.offset(skip).limit(limit).all()
        return [self._model_to_entity(model) for model in user_models]
    
    def _model_to_entity(self, model: UserModel) -> User:
        """Converte UserModel (ORM) para User (entidade de domínio)"""
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            roles=model.roles or [],
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
