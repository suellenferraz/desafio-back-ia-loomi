from langchain.tools import tool
from typing import Optional
import json
import time
from app.application.services.api_client import APIClient
from app.application.services.embedding_service import EmbeddingService
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


def create_paint_search_tool(
    api_client: APIClient,
    embedding_service: EmbeddingService
):
    @tool
    async def retrieve_paint_context(
        query: str,
        environment: Optional[str] = None
    ) -> str:
        """
        Busca tintas usando RAG (busca semântica).
        Gera embedding da query localmente e envia para back-api que faz busca semântica.
        Retorna informações detalhadas das tintas mais relevantes baseado na query do usuário.
        
        Args:
            query: Texto de busca (ex: "tinta branca para quarto", "azul externo")
            environment: "interno" ou "externo" (opcional, filtra resultados)
        
        Returns:
            JSON string com tintas encontradas e seus detalhes completos
        """
        start_time = time.time()
        logger.info(
            "paint_search_tool_started",
            tool="retrieve_paint_context",
            query=query,
            environment=environment
        )
        
        try:
            # 1. RAG: Gera embedding da query localmente
            logger.debug("generating_embedding", query=query)
            query_embedding = await embedding_service.generate_embedding(query)
            logger.debug("embedding_generated", embedding_size=len(query_embedding))
            
            # 2. Busca semântica no back-api (que faz similarity search no PostgreSQL)
            logger.info("semantic_search_started", environment=environment, top_k=5)
            paints_data = await api_client.search_semantic(
                query_embedding=query_embedding,
                environment=environment,
                top_k=5
            )
            
            if paints_data:
                elapsed_time = time.time() - start_time
                logger.info(
                    "paint_search_tool_success",
                    tool="retrieve_paint_context",
                    results_count=len(paints_data),
                    elapsed_time=round(elapsed_time, 3),
                    method="semantic_search"
                )
                return json.dumps(paints_data, ensure_ascii=False)
            
            # 3. Fallback: busca simples por texto se RAG não retornar resultados
            logger.warning("semantic_search_empty", falling_back_to="text_search")
            paints = await api_client.search_paints(query, environment)
            elapsed_time = time.time() - start_time
            logger.info(
                "paint_search_tool_success",
                tool="retrieve_paint_context",
                results_count=len(paints[:5]),
                elapsed_time=round(elapsed_time, 3),
                method="text_search_fallback"
            )
            return json.dumps(paints[:5], ensure_ascii=False)
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "paint_search_tool_error",
                tool="retrieve_paint_context",
                error=str(e),
                error_type=type(e).__name__,
                elapsed_time=round(elapsed_time, 3),
                exc_info=True
            )
            # Fallback final: busca simples na API
            logger.info("using_final_fallback", method="get_all_paints")
            paints = await api_client.get_all_paints(environment=environment, limit=10)
            return json.dumps(paints, ensure_ascii=False)
    
    return retrieve_paint_context
