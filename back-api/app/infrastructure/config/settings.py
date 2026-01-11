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

class SecuritySettings(BaseSettings):
    """Configurações de segurança e autenticação JWT"""
    model_config = SettingsConfigDict(env_prefix="SECURITY_")
    secret_key: str = Field(..., min_length=32, description="Chave secreta para JWT (mínimo 32 caracteres)")
    algorithm: str = Field(default="HS256", description="Algoritmo JWT")
    access_token_expire_minutes: int = Field(default=30, ge=1, le=1440, description="Tempo de expiração do token em minutos (1-1440)")

class Settings:
    """Classe principal de configurações"""
    def __init__(self):
        self.database = DatabaseSettings()
        self.app = AppSettings()
        self.server = ServerSettings()
        self.security = SecuritySettings()
    
    @property
    def database_url(self) -> str:
        """Retorna a URL do banco de dados"""
        return self.database.url

# Instância singleton
settings = Settings()
