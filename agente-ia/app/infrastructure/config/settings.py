from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class OpenAISettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="OPENAI_")
    api_key: str = Field(..., description="OpenAI API Key")
    model: str = Field(default="gpt-4o-mini", description="Modelo GPT")
    embedding_model: str = Field(default="text-embedding-3-small", description="Modelo de embeddings")


class APISettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="API_")
    base_url: str = Field(default="http://localhost:8000", description="URL base da API back-api")


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")
    url: str = Field(..., description="URL de conexão do PostgreSQL")


class Settings:
    def __init__(self):
        self.openai = OpenAISettings()
        self.api = APISettings()
        self.database = DatabaseSettings()
    
    @property
    def database_url(self) -> str:
        return self.database.url

settings = Settings()
