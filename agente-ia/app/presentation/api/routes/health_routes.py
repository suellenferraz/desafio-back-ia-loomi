from fastapi import APIRouter
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health_check():
    """
    Endpoint de health check para monitoramento do serviço.
    Retorna status do agente-ia e informações básicas.
    """
    logger.debug("health_check_requested")
    
    return {
        "status": "healthy",
        "service": "agente-ia",
        "version": "1.0.0"
    }


@router.get("/ready")
def readiness_check():
    """
    Endpoint de readiness check.
    Verifica se o serviço está pronto para receber requisições.
    """
    logger.debug("readiness_check_requested")
    
    # Verificar se dependências estão disponíveis
    try:
        from app.infrastructure.config.settings import settings
        
        # Verificar se OpenAI está configurado
        openai_configured = bool(settings.openai.api_key)
        
        # Verificar se API está configurada
        api_configured = bool(settings.api.base_url)
        
        if openai_configured and api_configured:
            logger.info("readiness_check_success")
            return {
                "status": "ready",
                "service": "agente-ia",
                "dependencies": {
                    "openai": "configured",
                    "api": "configured"
                }
            }
        else:
            logger.warning("readiness_check_failed", openai=openai_configured, api=api_configured)
            return {
                "status": "not_ready",
                "service": "agente-ia",
                "dependencies": {
                    "openai": "configured" if openai_configured else "missing",
                    "api": "configured" if api_configured else "missing"
                }
            }
    except Exception as e:
        logger.error("readiness_check_error", error=str(e), exc_info=True)
        return {
            "status": "error",
            "service": "agente-ia",
            "error": str(e)
        }
