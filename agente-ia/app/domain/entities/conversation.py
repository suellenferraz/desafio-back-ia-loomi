from dataclasses import dataclass
from datetime import datetime
from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from app.domain.entities.message import Message


@dataclass
class Conversation:
    id: UUID
    user_id: str
    messages: List["Message"]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(user_id: str) -> "Conversation":
        now = datetime.now()
        return Conversation(
            id=uuid4(),
            user_id=user_id,
            messages=[],
            created_at=now,
            updated_at=now
        )
