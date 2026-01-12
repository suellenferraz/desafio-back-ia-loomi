from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.paint import Paint
from app.domain.repositories.paint_repository import PaintRepository
from app.infrastructure.database.models.paint_model import PaintModel


class PaintRepositoryImpl(PaintRepository):
    """Implementação do repositório de Paint usando SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, paint: Paint) -> Paint:
        """Cria uma nova tinta"""
        paint_model = PaintModel(
            name=paint.name,
            color=paint.color,
            surface_type=paint.surface_type,
            environment=paint.environment,
            finish_type=paint.finish_type,
            features=paint.features,
            line=paint.line,
            created_at=paint.created_at,
            updated_at=paint.updated_at
        )
        self.db.add(paint_model)
        self.db.commit()
        self.db.refresh(paint_model)
        return self._model_to_entity(paint_model)
    
    def get_by_id(self, paint_id: int) -> Optional[Paint]:
        """Busca uma tinta por ID"""
        paint_model = self.db.query(PaintModel).filter(PaintModel.id == paint_id).first()
        if paint_model:
            return self._model_to_entity(paint_model)
        return None
    
    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        environment: Optional[str] = None,
        line: Optional[str] = None
    ) -> List[Paint]:
        """Lista todas as tintas com paginação e filtros opcionais"""
        query = self.db.query(PaintModel)
        
        if environment:
            query = query.filter(PaintModel.environment == environment)
        if line:
            query = query.filter(PaintModel.line == line)
        
        paint_models = query.offset(skip).limit(limit).all()
        return [self._model_to_entity(model) for model in paint_models]
    
    def update(self, paint_id: int, paint: Paint) -> Optional[Paint]:
        """Atualiza uma tinta existente"""
        paint_model = self.db.query(PaintModel).filter(PaintModel.id == paint_id).first()
        if not paint_model:
            return None
        
        paint_model.name = paint.name
        paint_model.color = paint.color
        paint_model.surface_type = paint.surface_type
        paint_model.environment = paint.environment
        paint_model.finish_type = paint.finish_type
        paint_model.features = paint.features
        paint_model.line = paint.line
        paint_model.updated_at = paint.updated_at
        
        self.db.commit()
        self.db.refresh(paint_model)
        return self._model_to_entity(paint_model)
    
    def delete(self, paint_id: int) -> bool:
        """Deleta uma tinta"""
        paint_model = self.db.query(PaintModel).filter(PaintModel.id == paint_id).first()
        if not paint_model:
            return False
        
        self.db.delete(paint_model)
        self.db.commit()
        return True
    
    def _model_to_entity(self, model: PaintModel) -> Paint:
        """Converte PaintModel (ORM) para Paint (entidade de domínio)"""
        return Paint(
            id=model.id,
            name=model.name,
            color=model.color,
            surface_type=model.surface_type,
            environment=model.environment,
            finish_type=model.finish_type,
            features=model.features or [],
            line=model.line,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
