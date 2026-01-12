from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import List, Optional
from datetime import datetime

class UserCreateSchema(BaseModel):
    """Schema para criação de usuário"""
    username: str = Field(..., min_length=3, max_length=50, description="Nome de usuário (mínimo 3 caracteres)")
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=8, max_length=100, description="Senha (mínimo 8 caracteres)")
    roles: Optional[List[str]] = Field(default=["user"], description="Lista de roles do usuário (padrão: ['user'])")
    
    @field_validator('roles')
    @classmethod
    def validate_roles(cls, v: Optional[List[str]]) -> List[str]:
        if v is None:
            return ["user"]
        
        valid_roles = ["user", "admin", "super_admin"]
        for role in v:
            if role not in valid_roles:
                raise ValueError(f"Role inválida: '{role}'. Roles válidas: {valid_roles}")
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Senha deve ter pelo menos 8 caracteres")
        return v
    
    model_config = {"json_schema_extra": {
        "example": {
            "username": "joao_silva",
            "email": "joao@example.com",
            "password": "senha_segura_123",
            "roles": ["user"]
        }
    }}


class UserLoginSchema(BaseModel):
    """Schema para login de usuário"""
    username: str = Field(..., description="Nome de usuário ou email")
    password: str = Field(..., description="Senha do usuário")
    
    model_config = {"json_schema_extra": {
        "example": {
            "username": "joao_silva",
            "password": "senha_segura_123"
        }
    }}


class TokenSchema(BaseModel):
    """Schema de resposta de token JWT"""
    access_token: str = Field(..., description="Token JWT de acesso")
    token_type: str = Field(default="bearer", description="Tipo do token")
    
    model_config = {"json_schema_extra": {
        "example": {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
    }}


class UserResponseSchema(BaseModel):
    """Schema de resposta de usuário (sem senha)"""
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "username": "joao_silva",
                "email": "joao@example.com",
                "roles": ["user"],
                "is_active": True,
                "created_at": "2024-01-10T10:00:00Z",
                "updated_at": "2024-01-10T10:00:00Z"
            }
        }
    )
    
    id: int
    username: str
    email: str
    roles: List[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserWithTokenSchema(BaseModel):
    """Schema de resposta de usuário com token"""
    user: UserResponseSchema
    token: TokenSchema
    
    model_config = {"json_schema_extra": {
        "example": {
            "user": {
                "id": 1,
                "username": "joao_silva",
                "email": "joao@example.com",
                "roles": ["user"],
                "is_active": True,
                "created_at": "2024-01-10T10:00:00Z",
                "updated_at": "2024-01-10T10:00:00Z"
            },
            "token": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    }}


class PasswordChangeSchema(BaseModel):
    """Schema para mudança de senha (próprio usuário)"""
    current_password: str = Field(..., min_length=8, description="Senha atual")
    new_password: str = Field(..., min_length=8, max_length=100, description="Nova senha (mínimo 8 caracteres)")
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Nova senha deve ter pelo menos 8 caracteres")
        return v
    
    model_config = {"json_schema_extra": {
        "example": {
            "current_password": "senha_atual_123",
            "new_password": "nova_senha_segura_123"
        }
    }}


class UserUpdateSchema(BaseModel):
    """Schema para atualização de usuário (administrativo)"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Nome de usuário (mínimo 3 caracteres)")
    email: Optional[EmailStr] = Field(None, description="Email do usuário")
    roles: Optional[List[str]] = Field(None, description="Lista de roles do usuário")
    
    @field_validator('roles')
    @classmethod
    def validate_roles(cls, v: Optional[List[str]]) -> List[str]:
        if v is None:
            return v
        
        valid_roles = ["user", "admin", "super_admin"]
        for role in v:
            if role not in valid_roles:
                raise ValueError(f"Role inválida: '{role}'. Roles válidas: {valid_roles}")
        return v
    
    model_config = {"json_schema_extra": {
        "example": {
            "username": "joao_silva_atualizado",
            "email": "joao.novo@example.com",
            "roles": ["user", "admin"]
        }
    }}


class UserPasswordAdminSchema(BaseModel):
    """Schema para definir senha de usuário (administrativo)"""
    password: str = Field(..., min_length=8, max_length=100, description="Nova senha (mínimo 8 caracteres)")
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Senha deve ter pelo menos 8 caracteres")
        return v
    
    model_config = {"json_schema_extra": {
        "example": {
            "password": "nova_senha_segura_123"
        }
    }}
