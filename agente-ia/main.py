from dotenv import load_dotenv
load_dotenv()

# Inicializar logging estruturado antes de qualquer import
from app.infrastructure.logging.logger import setup_logging
setup_logging()

from fastapi import FastAPI
from app.presentation.api.routes import chat_routes, health_routes

app = FastAPI(
    title="Agente IA - Tintas Suvinil",
    description="Agente inteligente especializado em recomendar tintas Suvinil",
    version="1.0.0"
)

app.include_router(chat_routes.router, prefix="/api/v1")
app.include_router(health_routes.router, prefix="/api/v1")

@app.get("/", tags=["General"])
def root():
    return {
        "message": "Agente IA - Tintas Suvinil",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }
