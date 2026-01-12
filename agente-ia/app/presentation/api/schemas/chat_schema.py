from pydantic import BaseModel, Field
from typing import List, Optional


class MessageSchema(BaseModel):
    role: str = Field(..., description="Role da mensagem: 'user' ou 'assistant'")
    content: str = Field(..., description="Conteúdo da mensagem")


class ChatRequestSchema(BaseModel):
    message: str = Field(..., min_length=1, description="Mensagem do usuário")
    conversation_id: Optional[str] = Field(None, description="ID da conversa (opcional)")


class ChatResponseSchema(BaseModel):
    response: str = Field(..., description="Resposta do agente")
    conversation_id: str = Field(..., description="ID da conversa")
    reasoning: Optional[str] = Field(None, description="Raciocínio do agente")
    tools_used: Optional[List[str]] = Field(None, description="Ferramentas utilizadas")
