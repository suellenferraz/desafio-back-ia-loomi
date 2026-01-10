from fastapi import FastAPI
from app.presentation.api.routes import product_routes

app = FastAPI(
    title="API Tintas",
    description="Esta API é responsável por gerenciar as tintas da empresa",
    version="1.0.0"
)

# Registra as rotas
app.include_router(product_routes.router)

@app.get("/")
def root():
    """Endpoint raiz da API"""
    return {
        "message": "API Tintas",
        "docs": "/docs"
    }

