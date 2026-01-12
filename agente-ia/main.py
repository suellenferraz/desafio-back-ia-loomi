from dotenv import load_dotenv
load_dotenv()

# Inicializar logging estruturado antes de qualquer import
from app.infrastructure.logging.logger import setup_logging
setup_logging()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.api.routes import chat_routes, health_routes
from app.infrastructure.database.connection import Base, engine

# Criar tabelas no startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agente IA - Tintas Suvinil",
    description="Agente inteligente especializado em recomendar tintas Suvinil",
    version="1.0.0"
)

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
