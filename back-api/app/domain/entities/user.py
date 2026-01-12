from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class User:
    """Entidade de domínio User (Usuário)"""
    id: int
    username: str
    email: str
    password_hash: str  # Sempre hash, nunca senha em texto plano
    roles: List[str]  # Ex: ["user"], ["admin"], ["user", "admin"]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        """Validações básicas após inicialização"""
        # Validar que tem pelo menos uma role
        if not self.roles:
            raise ValueError("User deve ter pelo menos uma role")
        
        # Validar roles válidas
        valid_roles = ["user", "admin", "super_admin"]
        for role in self.roles:
            if role not in valid_roles:
                raise ValueError(
                    f"Role inválida: '{role}'. "
                    f"Roles válidas: {valid_roles}"
                )
        
        # Validar email (validação básica)
        if "@" not in self.email or "." not in self.email.split("@")[1]:
            raise ValueError(f"Email inválido: {self.email}")
