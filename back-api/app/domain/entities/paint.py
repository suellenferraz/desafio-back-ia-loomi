from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Paint:
    """Entidade de domínio Paint (Tinta)"""
    id: int
    name: str
    color: str
    surface_type: str  # Ex: "Parede", "Madeira", "Metal"
    environment: str  # "interno" ou "externo"
    finish_type: str  # Ex: "Fosco", "Semi-brilho", "Brilho"
    features: List[str]  # Ex: ["lavável", "anti-mofo", "sem odor"]
    line: str  # Ex: "Premium", "Standard"
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        """Validações básicas após inicialização"""
        if self.environment not in ["interno", "externo"]:
            raise ValueError(
                f"Environment deve ser 'interno' ou 'externo', "
                f"recebido: {self.environment}"
            )
