from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class DatabaseSettings(BaseSettings):
    """Configurações de banco de dados"""
    model_config = SettingsConfigDict(env_prefix="DB_")
    url: str = Field(..., description="URL de conexão do PostgreSQL")
    pool_size: int = Field(default=5, description="Tamanho do pool de conexões")
    max_overflow: int = Field(default=10, description="Máximo de overflow do pool")

class AppSettings(BaseSettings):
    """Configurações gerais da aplicação"""
    
    model_config = SettingsConfigDict(env_prefix="APP_")
    name: str = Field(default="API Tintas", description="Nome da aplicação")
    version: str = Field(default="1.0.0", description="Versão da aplicação")
    environment: str = Field(default="development", description="Ambiente de execução")

class ServerSettings(BaseSettings):
    """Configurações do servidor"""
    model_config = SettingsConfigDict(env_prefix="SERVER_")
    host: str = Field(default="0.0.0.0", description="Host do servidor")
    port: int = Field(default=8000, description="Porta do servidor")

class Settings:
    """Classe principal de configurações"""
    def __init__(self):
        self.database = DatabaseSettings()
        self.app = AppSettings()
        self.server = ServerSettings()
    
    @property
    def database_url(self) -> str:
        """Retorna a URL do banco de dados"""
        return self.database.url

# Instância singleton
settings = Settings()
