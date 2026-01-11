from dataclasses import dataclass
from datetime import datetime

@dataclass
class Session:
    """Entidade de domínio Session (Sessão de usuário)"""
    id: int
    user_id: int
    session_id: str  # ID único da sessão (usado no JWT)
    expires_at: datetime
    created_at: datetime
