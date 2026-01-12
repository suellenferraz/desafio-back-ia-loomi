from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.paint import Paint

class PaintRepository(ABC):
    """Interface abstrata para repositório de Paint"""
    
    @abstractmethod
    def create(self, paint: Paint) -> Paint:
        """Cria uma nova tinta"""
        pass
    
    @abstractmethod
    def get_by_id(self, paint_id: int) -> Optional[Paint]:
        """Busca uma tinta por ID"""
        pass
    
    @abstractmethod
    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        environment: Optional[str] = None,
        line: Optional[str] = None
    ) -> List[Paint]:
        """Lista todas as tintas com paginação e filtros opcionais"""
        pass
    
    @abstractmethod
    def update(self, paint_id: int, paint: Paint) -> Optional[Paint]:
        """Atualiza uma tinta existente"""
        pass
    
    @abstractmethod
    def delete(self, paint_id: int) -> bool:
        """Deleta uma tinta"""
        pass
    
    @abstractmethod
    def search_semantic(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        environment: Optional[str] = None
    ) -> List[Paint]:
        """Busca semântica usando embeddings (pgvector)"""
        pass
    
    @abstractmethod
    def update_embedding(self, paint_id: int, embedding: List[float]) -> bool:
        """Atualiza o embedding de uma tinta"""
        pass
