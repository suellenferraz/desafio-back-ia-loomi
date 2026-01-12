from typing import List
import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Serviço para geração de embeddings usando OpenAI"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = "text-embedding-3-small"
        self.client = None
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            logger.warning("EmbeddingService criado sem API key")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Gera embedding para um texto.
        
        Args:
            text: Texto para gerar embedding
            
        Returns:
            Lista de floats (embedding)
            
        Raises:
            ValueError: Se não houver cliente configurado ou texto vazio
            Exception: Se houver erro na chamada à API
        """
        if not self.client:
            error_msg = "EmbeddingService não configurado: OPENAI_API_KEY não encontrada"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        if not text or not text.strip():
            error_msg = "Texto vazio não pode gerar embedding"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text.strip()
            )
            embedding = response.data[0].embedding
            logger.info(f"Embedding gerado com sucesso: text_length={len(text)}, embedding_size={len(embedding)}")
            return embedding
        except Exception as e:
            logger.error(f"Erro ao gerar embedding: {str(e)}", exc_info=True)
            raise
    
    def generate_embedding_for_paint(
        self,
        name: str,
        color: str,
        surface_type: str,
        environment: str,
        finish_type: str,
        features: List[str],
        line: str
    ) -> List[float]:
        """
        Gera embedding para uma tinta combinando todas as informações.
        
        Args:
            name: Nome da tinta
            color: Cor
            surface_type: Tipo de superfície
            environment: Ambiente (interno/externo)
            finish_type: Tipo de acabamento
            features: Lista de features
            line: Linha da tinta
            
        Returns:
            Lista de floats (embedding)
            
        Raises:
            ValueError: Se não conseguir gerar embedding
        """
        # Combinar todas as informações em um texto
        text_parts = [
            name or "",
            color or "",
            surface_type or "",
            environment or "",
            finish_type or "",
            line or "",
        ]
        
        # Adicionar features
        if features:
            text_parts.extend([f for f in features if f])
        
        # Combinar tudo
        text = " ".join(filter(None, text_parts))
        
        return self.generate_embedding(text)
