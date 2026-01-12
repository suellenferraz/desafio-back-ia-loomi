from fastapi import APIRouter, Depends, HTTPException
import time
from app.presentation.api.schemas.chat_schema import ChatRequestSchema, ChatResponseSchema
from app.presentation.api.dependencies.agent_dependencies import get_paint_agent
from app.application.agents.paint_agent import PaintAgent
from app.domain.repositories.conversation_repository import ConversationRepository
from app.infrastructure.repositories.conversation_repository_impl import ConversationRepositoryImpl
from app.domain.entities.conversation import Conversation
from app.infrastructure.logging.logger import get_logger
from uuid import UUID

logger = get_logger(__name__)
router = APIRouter(prefix="/chat", tags=["Chat"])


def get_conversation_repository() -> ConversationRepository:
    return ConversationRepositoryImpl()


def validate_user_input(message: str) -> bool:
    """
    Valida entrada do usuário para prevenir prompt injection e garantir segurança.
    
    Args:
        message: Mensagem do usuário
        
    Returns:
        True se válida, False se suspeita
    """
    # Padrões suspeitos de prompt injection
    suspicious_patterns = [
        "ignore previous instructions",
        "forget everything",
        "you are now",
        "system:",
        "assistant:",
        "ignore all",
        "disregard",
        "override",
        "bypass"
    ]
    
    message_lower = message.lower()
    for pattern in suspicious_patterns:
        if pattern in message_lower:
            logger.warning("suspicious_input_detected", pattern=pattern, message_preview=message[:50])
            return False
    
    # Limite de tamanho para prevenir abuso
    if len(message) > 2000:
        logger.warning("message_too_long", length=len(message))
        return False
    
    # Verificar se não está vazia ou só espaços
    if not message.strip():
        logger.warning("empty_message")
        return False
    
    return True


@router.post("", response_model=ChatResponseSchema)
async def chat(
    request: ChatRequestSchema,
    agent: PaintAgent = Depends(get_paint_agent),
    conversation_repo: ConversationRepository = Depends(get_conversation_repository)
):
    """
    Endpoint principal para chat com o agente de IA.
    Valida entrada, processa mensagem e retorna resposta com observabilidade.
    """
    start_time = time.time()
    logger.info(
        "chat_request_received",
        message_length=len(request.message),
        has_conversation_id=bool(request.conversation_id)
    )
    
    # Validação de segurança
    if not validate_user_input(request.message):
        logger.warning("chat_request_rejected", reason="invalid_input")
        raise HTTPException(
            status_code=400,
            detail="Mensagem inválida ou contém padrões suspeitos. Por favor, reformule sua pergunta."
        )
    
    # Buscar ou criar conversa
    conversation_id = request.conversation_id
    if conversation_id:
        try:
            conversation = conversation_repo.get_by_id(UUID(conversation_id))
            logger.debug("conversation_found", conversation_id=str(conversation_id))
        except Exception as e:
            logger.warning("conversation_not_found", conversation_id=conversation_id, error=str(e))
            conversation = None
    else:
        conversation = None

    if not conversation:
        conversation = Conversation.create(user_id="anonymous")
        conversation = conversation_repo.create(conversation)
        logger.info("conversation_created", conversation_id=str(conversation.id))

    # Preparar histórico (últimas 10 mensagens)
    chat_history = [
        {"role": msg.role, "content": msg.content}
        for msg in conversation.messages[-10:]
    ]
    logger.debug("chat_history_prepared", history_length=len(chat_history))

    try:
        # Invocar agente (agora retorna Dict com observabilidade)
        result = await agent.invoke(request.message, chat_history)

        # Salvar mensagens na conversa
        from app.domain.entities.message import Message
        user_message = Message.create(conversation.id, "user", request.message)
        assistant_message = Message.create(conversation.id, "assistant", result["output"])

        conversation.messages.append(user_message)
        conversation.messages.append(assistant_message)
        conversation_repo.update(conversation)

        elapsed_time = time.time() - start_time
        logger.info(
            "chat_request_success",
            conversation_id=str(conversation.id),
            response_length=len(result["output"]),
            tools_used=result.get("tools_used", []),
            elapsed_time=round(elapsed_time, 3)
        )

        # Retornar resposta com observabilidade
        return ChatResponseSchema(
            response=result["output"],
            conversation_id=str(conversation.id),
            reasoning=result.get("reasoning"),
            tools_used=result.get("tools_used", [])
        )
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        logger.error(
            "chat_request_error",
            error=str(e),
            error_type=type(e).__name__,
            elapsed_time=round(elapsed_time, 3),
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Erro ao processar sua mensagem. Tente novamente."
        )
