from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.domain.entities.paint import Paint
from app.domain.repositories.paint_repository import PaintRepository


def create_paint(
    repository: PaintRepository,
    name: str,
    color: str,
    surface_type: str,
    environment: str,
    finish_type: str,
    features: List[str],
    line: str
) -> Paint:
    """Cria uma nova tinta"""
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
    return repository.create(paint)


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
    line: str
) -> Optional[Paint]:
    """Atualiza uma tinta existente"""
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
    return repository.update(paint_id, updated_paint)


def delete_paint(repository: PaintRepository, paint_id: int) -> bool:
    """Deleta uma tinta"""
    return repository.delete(paint_id)
