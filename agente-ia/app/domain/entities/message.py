from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Message:
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    tool_calls: Optional[list] = None
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    @staticmethod
    def create(conversation_id: UUID, role: str, content: str, tool_calls: Optional[list] = None) -> "Message":
        return Message(
            id=uuid4(),
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls
        )
