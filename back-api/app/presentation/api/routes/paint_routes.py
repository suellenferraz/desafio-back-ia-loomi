from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.domain.repositories.paint_repository import PaintRepository
from app.application.use_cases.paint_use_cases import (
    create_paint as create_paint_uc,
    get_paint_by_id as get_paint_by_id_uc,
    get_all_paints as get_all_paints_uc,
    update_paint as update_paint_uc,
    delete_paint as delete_paint_uc,
    search_semantic_paints
)
from app.presentation.api.schemas.paint_schema import (
    PaintCreateSchema,
    PaintUpdateSchema,
    PaintResponseSchema,
    PaintSearchSchema
)
from app.presentation.api.dependencies.auth_dependencies import get_paint_repository, get_embedding_service

router = APIRouter(prefix="/paints", tags=["Paints"])

@router.post("", response_model=PaintResponseSchema, status_code=201)
def create_paint(
    paint_data: PaintCreateSchema,
    repository: PaintRepository = Depends(get_paint_repository),
    embedding_service = Depends(get_embedding_service)
):
    """Cria uma nova tinta e gera embedding automaticamente"""
    try:
        paint = create_paint_uc(
            repository=repository,
            name=paint_data.name,
            color=paint_data.color,
            surface_type=paint_data.surface_type,
            environment=paint_data.environment,
            finish_type=paint_data.finish_type,
            features=paint_data.features,
            line=paint_data.line,
            embedding_service=embedding_service
        )
        return PaintResponseSchema.model_validate(paint)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{paint_id}", response_model=PaintResponseSchema)
def get_paint_by_id(
    paint_id: int,
    repository: PaintRepository = Depends(get_paint_repository)
):
    """Busca uma tinta por ID"""
    paint = get_paint_by_id_uc(repository=repository, paint_id=paint_id)
    if not paint:
        raise HTTPException(status_code=404, detail=f"Tinta com ID {paint_id} não encontrada")
    return PaintResponseSchema.model_validate(paint)


@router.get("", response_model=List[PaintResponseSchema])
def get_all_paints(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    environment: Optional[str] = Query(None, description="Filtrar por ambiente: 'interno' ou 'externo'"),
    line: Optional[str] = Query(None, description="Filtrar por linha"),
    repository: PaintRepository = Depends(get_paint_repository)
):
    """Lista todas as tintas com paginação e filtros opcionais"""
    paints = get_all_paints_uc(
        repository=repository,
        skip=skip,
        limit=limit,
        environment=environment,
        line=line
    )
    return [PaintResponseSchema.model_validate(paint) for paint in paints]


@router.put("/{paint_id}", response_model=PaintResponseSchema)
def update_paint(
    paint_id: int,
    paint_data: PaintUpdateSchema,
    repository: PaintRepository = Depends(get_paint_repository),
    embedding_service = Depends(get_embedding_service)
):
    """Atualiza uma tinta existente e regenera embedding automaticamente"""
    # Busca a tinta existente para pegar os valores atuais
    existing_paint = get_paint_by_id_uc(repository=repository, paint_id=paint_id)
    if not existing_paint:
        raise HTTPException(status_code=404, detail=f"Tinta com ID {paint_id} não encontrada")
    
    # Usa valores do schema ou mantém os existentes
    updated_paint = update_paint_uc(
        repository=repository,
        paint_id=paint_id,
        name=paint_data.name or existing_paint.name,
        color=paint_data.color or existing_paint.color,
        surface_type=paint_data.surface_type or existing_paint.surface_type,
        environment=paint_data.environment or existing_paint.environment,
        finish_type=paint_data.finish_type or existing_paint.finish_type,
        features=paint_data.features if paint_data.features is not None else existing_paint.features,
        line=paint_data.line or existing_paint.line,
        embedding_service=embedding_service
    )
    
    if not updated_paint:
        raise HTTPException(status_code=404, detail=f"Tinta com ID {paint_id} não encontrada")
    
    return PaintResponseSchema.model_validate(updated_paint)


@router.delete("/{paint_id}", status_code=204)
def delete_paint(
    paint_id: int,
    repository: PaintRepository = Depends(get_paint_repository)
):
    """Deleta uma tinta"""
    deleted = delete_paint_uc(repository=repository, paint_id=paint_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Tinta com ID {paint_id} não encontrada")
    return None


@router.post("/search", response_model=List[PaintResponseSchema])
def search_paints_semantic(
    search_data: PaintSearchSchema,
    repository: PaintRepository = Depends(get_paint_repository)
):
    """Busca semântica de tintas usando embeddings (RAG)"""
    try:
        paints = search_semantic_paints(
            repository=repository,
            query_embedding=search_data.embedding,
            top_k=search_data.top_k,
            environment=search_data.environment
        )
        return [PaintResponseSchema.model_validate(paint) for paint in paints]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca semântica: {str(e)}")
