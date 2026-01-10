from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from app.infrastructure.config.settings import settings

# Base para models
Base = declarative_base()

# Engine do SQLAlchemy
engine = create_engine(
    settings.database_url,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    pool_pre_ping=True,  # Verifica conexões antes de usar
    echo=False  # True para ver SQL no console (desenvolvimento)
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """
    Dependency injection para obter sessão do banco de dados.
    Usado pelo FastAPI para injetar sessão nas rotas.
    
    Yields:
        Session: Sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializa o banco de dados (cria tabelas)"""
    Base.metadata.create_all(bind=engine)
