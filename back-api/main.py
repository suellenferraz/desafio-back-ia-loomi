from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.presentation.api.routes import product_routes, health_routes

app = FastAPI(
    title="API Tintas",
    description="Esta API é responsável por gerenciar as tintas da empresa",
    version="1.0.0"
)

app.include_router(product_routes.router)
app.include_router(health_routes.router)

@app.get("/")
def root():
    return {
        "message": "API Tintas",
        "docs": "/docs"
    }

