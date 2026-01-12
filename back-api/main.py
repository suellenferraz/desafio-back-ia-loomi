from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.presentation.api.routes import product_routes, health_routes, paint_routes, account_routes, user_routes

app = FastAPI(
    title="API Tintas",
    description="Esta API é responsável por gerenciar as tintas da empresa",
    version="1.0.0",
    tags_metadata=[
        {
            "name": "General",
            "description": "Endpoints gerais da aplicação",
        },
        {
            "name": "Products",
            "description": "Exemplo de endpoint de produtos",
        },
        {
            "name": "Paints",
            "description": "Operações CRUD para gerenciar tintas Suvinil",
        },
        {
            "name": "Account",
            "description": "Autenticação JWT: signup, login, logout e alteração de senha",
        },
        {
            "name": "Users",
            "description": "Gerenciamento administrativo de usuários (apenas admin/super_admin)",
        },
    ]
)

app.include_router(health_routes.router, prefix="/api/v1")
app.include_router(product_routes.router, prefix="/api/v1")
app.include_router(paint_routes.router, prefix="/api/v1")
app.include_router(account_routes.router, prefix="/api/v1")
app.include_router(user_routes.router, prefix="/api/v1") 

@app.get("/", tags=["General"], summary="Redirect To Docs")
def root():
    return {
        "message": "API Tintas",
        "version": "1.0.0",
        "docs": "/docs",
        "api": "/api/v1"
    }

