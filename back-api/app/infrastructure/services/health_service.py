from sqlalchemy import text
from app.infrastructure.database.connection import engine

def check_database_health() -> str:
    """
    Verifica saúde da conexão com banco de dados.
    
    Returns:
        str: "connected" ou "disconnected"
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "connected"
    except Exception:
        return "disconnected"

def get_health_status() -> dict:
    """
    Retorna status geral da aplicação.
    
    Returns:
        dict: Status da aplicação e banco
    """
    db_status = check_database_health()
    
    if db_status == "connected":
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Application and database are running"
        }
    else:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "message": "Database connection failed"
        }
