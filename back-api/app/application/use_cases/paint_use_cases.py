from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.domain.entities.paint import Paint
from app.domain.repositories.paint_repository import PaintRepository
from app.infrastructure.services.embedding_service import EmbeddingService


def create_paint(
    repository: PaintRepository,
    name: str,
    color: str,
    surface_type: str,
    environment: str,
    finish_type: str,
    features: List[str],
    line: str,
    embedding_service: EmbeddingService
) -> Paint:
    """
    Cria uma nova tinta e gera embedding automaticamente.
    
    Args:
        repository: Repositório de tintas
        name: Nome da tinta
        color: Cor
        surface_type: Tipo de superfície
        environment: Ambiente (interno/externo)
        finish_type: Tipo de acabamento
        features: Lista de features
        line: Linha da tinta
        embedding_service: Serviço para gerar embeddings (obrigatório)
    
    Returns:
        Paint: Tinta criada
        
    Raises:
        ValueError: Se não conseguir gerar embedding
    """
    now = datetime.now()
    paint = Paint(
        id=0,  # Será definido pelo banco
        name=name,
        color=color,
        surface_type=surface_type,
        environment=environment,
        finish_type=finish_type,
        features=features,
        line=line,
        created_at=now,
        updated_at=now
    )
    
    # Criar tinta no banco
    created_paint = repository.create(paint)
    
    # Gerar embedding automaticamente (obrigatório)
    try:
        embedding = embedding_service.generate_embedding_for_paint(
            name=created_paint.name,
            color=created_paint.color,
            surface_type=created_paint.surface_type,
            environment=created_paint.environment,
            finish_type=created_paint.finish_type,
            features=created_paint.features,
            line=created_paint.line
        )
        repository.update_embedding(created_paint.id, embedding)
    except Exception as e:
        # Se falhar ao gerar embedding, deletar a tinta criada
        repository.delete(created_paint.id)
        raise ValueError(f"Erro ao gerar embedding para a tinta: {str(e)}")
    
    return created_paint


def get_paint_by_id(repository: PaintRepository, paint_id: int) -> Optional[Paint]:
    """Busca uma tinta por ID"""
    return repository.get_by_id(paint_id)


def get_all_paints(
    repository: PaintRepository,
    skip: int = 0,
    limit: int = 100,
    environment: Optional[str] = None,
    line: Optional[str] = None
) -> List[Paint]:
    """Lista todas as tintas com paginação e filtros opcionais"""
    return repository.get_all(skip=skip, limit=limit, environment=environment, line=line)


def update_paint(
    repository: PaintRepository,
    paint_id: int,
    name: str,
    color: str,
    surface_type: str,
    environment: str,
    finish_type: str,
    features: List[str],
    line: str,
    embedding_service: EmbeddingService
) -> Optional[Paint]:
    """
    Atualiza uma tinta existente e regenera embedding automaticamente.
    
    Args:
        repository: Repositório de tintas
        paint_id: ID da tinta
        name: Nome da tinta
        color: Cor
        surface_type: Tipo de superfície
        environment: Ambiente (interno/externo)
        finish_type: Tipo de acabamento
        features: Lista de features
        line: Linha da tinta
        embedding_service: Serviço para gerar embeddings (obrigatório)
    
    Returns:
        Paint atualizada ou None se não encontrada
        
    Raises:
        ValueError: Se não conseguir regenerar embedding
    """
    existing_paint = repository.get_by_id(paint_id)
    if not existing_paint:
        return None
    
    updated_paint = Paint(
        id=paint_id,
        name=name,
        color=color,
        surface_type=surface_type,
        environment=environment,
        finish_type=finish_type,
        features=features,
        line=line,
        created_at=existing_paint.created_at,
        updated_at=datetime.now()
    )
    
    result = repository.update(paint_id, updated_paint)
    
    # Regenerar embedding (obrigatório)
    if result:
        try:
            embedding = embedding_service.generate_embedding_for_paint(
                name=result.name,
                color=result.color,
                surface_type=result.surface_type,
                environment=result.environment,
                finish_type=result.finish_type,
                features=result.features,
                line=result.line
            )
            repository.update_embedding(result.id, embedding)
        except Exception as e:
            raise ValueError(f"Erro ao regenerar embedding para a tinta: {str(e)}")
    
    return result


def delete_paint(repository: PaintRepository, paint_id: int) -> bool:
    """Deleta uma tinta"""
    return repository.delete(paint_id)


def search_semantic_paints(
    repository: PaintRepository,
    query_embedding: List[float],
    top_k: int = 5,
    environment: Optional[str] = None
) -> List[Paint]:
    """Busca semântica de tintas usando embeddings"""
    return repository.search_semantic(
        query_embedding=query_embedding,
        top_k=top_k,
        environment=environment
    )
