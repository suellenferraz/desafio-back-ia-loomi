from fastapi import APIRouter
from app.presentation.api.schemas.health_schema import HealthResponse
from app.infrastructure.services.health_service import get_health_status

router = APIRouter(prefix="/health", tags=["health"])

@router.get("", response_model=HealthResponse)
def health_check():
    """Health check endpoint - verifica status da aplicação e banco"""
    return get_health_status()
