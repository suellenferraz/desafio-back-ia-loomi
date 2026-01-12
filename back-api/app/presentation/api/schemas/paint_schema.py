from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional
from datetime import datetime

class PaintCreateSchema(BaseModel):
    """Schema para criação de tinta"""
    name: str = Field(..., min_length=1, max_length=200, description="Nome da tinta")
    color: str = Field(..., min_length=1, max_length=50, description="Cor da tinta")
    surface_type: str = Field(..., min_length=1, max_length=100, description="Tipo de superfície")
    environment: str = Field(..., description="Ambiente: 'interno' ou 'externo'")
    finish_type: str = Field(..., min_length=1, max_length=50, description="Tipo de acabamento")
    features: List[str] = Field(default_factory=list, description="Lista de features")
    line: str = Field(..., min_length=1, max_length=50, description="Linha da tinta")
    
    @field_validator('environment')
    @classmethod
    def validate_environment(cls, v: str) -> str:
        if v not in ["interno", "externo"]:
            raise ValueError("Environment deve ser 'interno' ou 'externo'")
        return v
    
    model_config = {"json_schema_extra": {
        "example": {
            "name": "Suvinil Premium Branco Neve",
            "color": "Branco",
            "surface_type": "Parede",
            "environment": "interno",
            "finish_type": "Fosco",
            "features": ["lavável", "sem odor", "cobrimento excelente"],
            "line": "Premium"
        }
    }}


class PaintUpdateSchema(BaseModel):
    """Schema para atualização de tinta"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Nome da tinta")
    color: Optional[str] = Field(None, min_length=1, max_length=50, description="Cor da tinta")
    surface_type: Optional[str] = Field(None, min_length=1, max_length=100, description="Tipo de superfície")
    environment: Optional[str] = Field(None, description="Ambiente: 'interno' ou 'externo'")
    finish_type: Optional[str] = Field(None, min_length=1, max_length=50, description="Tipo de acabamento")
    features: Optional[List[str]] = Field(None, description="Lista de features")
    line: Optional[str] = Field(None, min_length=1, max_length=50, description="Linha da tinta")
    
    @field_validator('environment')
    @classmethod
    def validate_environment(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ["interno", "externo"]:
            raise ValueError("Environment deve ser 'interno' ou 'externo'")
        return v


class PaintResponseSchema(BaseModel):
    """Schema de resposta de tinta"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    color: str
    surface_type: str
    environment: str
    finish_type: str
    features: List[str]
    line: str
    created_at: datetime
    updated_at: datetime

class PaintSearchSchema(BaseModel):
    """Schema para busca semântica de tintas"""
    embedding: List[float] = Field(..., description="Embedding da query (vetor de floats)")
    top_k: int = Field(5, ge=1, le=50, description="Número de resultados desejados")
    environment: Optional[str] = Field(None, description="Filtrar por ambiente: 'interno' ou 'externo'")
    
    @field_validator('environment')
    @classmethod
    def validate_environment(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ["interno", "externo"]:
            raise ValueError("Environment deve ser 'interno' ou 'externo'")
        return v
    
    model_config = {"json_schema_extra": {
        "example": {
            "embedding": [0.1, 0.2, 0.3, 0.4, 0.5],
            "top_k": 5,
            "environment": "interno"
        }
    }}
