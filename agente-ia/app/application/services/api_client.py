from typing import List, Dict, Optional
import httpx
import time
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, timeout=30.0)
        logger.info("api_client_initialized", base_url=base_url)

    async def get_all_paints(
        self,
        environment: Optional[str] = None,
        line: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict]:
        start_time = time.time()
        params = {"skip": skip, "limit": limit}
        if environment:
            params["environment"] = environment
        if line:
            params["line"] = line

        try:
            logger.debug("api_request_started", method="GET", endpoint="/api/v1/paints", params=params)
            response = await self.client.get("/api/v1/paints", params=params)
            response.raise_for_status()
            result = response.json()
            elapsed_time = time.time() - start_time
            logger.info(
                "api_request_success",
                method="GET",
                endpoint="/api/v1/paints",
                status_code=response.status_code,
                results_count=len(result) if isinstance(result, list) else 1,
                elapsed_time=round(elapsed_time, 3)
            )
            return result
        except httpx.HTTPStatusError as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "api_request_http_error",
                method="GET",
                endpoint="/api/v1/paints",
                status_code=e.response.status_code,
                detail=e.response.text,
                elapsed_time=round(elapsed_time, 3),
                exc_info=True
            )
            raise
        except httpx.RequestError as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "api_request_network_error",
                method="GET",
                endpoint="/api/v1/paints",
                error=str(e),
                elapsed_time=round(elapsed_time, 3),
                exc_info=True
            )
            raise

    async def get_paint_by_id(self, paint_id: int) -> Dict:
        start_time = time.time()
        try:
            logger.debug("api_request_started", method="GET", endpoint=f"/api/v1/paints/{paint_id}")
            response = await self.client.get(f"/api/v1/paints/{paint_id}")
            response.raise_for_status()
            result = response.json()
            elapsed_time = time.time() - start_time
            logger.info(
                "api_request_success",
                method="GET",
                endpoint=f"/api/v1/paints/{paint_id}",
                status_code=response.status_code,
                elapsed_time=round(elapsed_time, 3)
            )
            return result
        except httpx.HTTPStatusError as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "api_request_http_error",
                method="GET",
                endpoint=f"/api/v1/paints/{paint_id}",
                status_code=e.response.status_code,
                elapsed_time=round(elapsed_time, 3),
                exc_info=True
            )
            raise
        except httpx.RequestError as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "api_request_network_error",
                method="GET",
                endpoint=f"/api/v1/paints/{paint_id}",
                error=str(e),
                elapsed_time=round(elapsed_time, 3),
                exc_info=True
            )
            raise

    async def search_semantic(
        self,
        query_embedding: List[float],
        environment: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Busca semântica via endpoint do back-api.
        O back-api faz similarity search no PostgreSQL (pgvector) e retorna tintas relevantes.
        
        Args:
            query_embedding: Embedding da query do usuário (gerado localmente)
            environment: "interno" ou "externo" (opcional)
            top_k: Número de resultados desejados
        
        Returns:
            Lista de tintas encontradas
        """
        payload = {
            "embedding": query_embedding,
            "top_k": top_k
        }
        if environment:
            payload["environment"] = environment
        
        start_time = time.time()
        try:
            logger.debug(
                "api_request_started",
                method="POST",
                endpoint="/api/v1/paints/search",
                embedding_size=len(query_embedding),
                top_k=top_k,
                environment=environment
            )
            response = await self.client.post(
                "/api/v1/paints/search",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            elapsed_time = time.time() - start_time
            logger.info(
                "api_request_success",
                method="POST",
                endpoint="/api/v1/paints/search",
                status_code=response.status_code,
                results_count=len(result) if isinstance(result, list) else 1,
                elapsed_time=round(elapsed_time, 3)
            )
            return result
        except httpx.HTTPStatusError as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "api_request_http_error",
                method="POST",
                endpoint="/api/v1/paints/search",
                status_code=e.response.status_code,
                elapsed_time=round(elapsed_time, 3),
                exc_info=True
            )
            raise
        except httpx.RequestError as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "api_request_network_error",
                method="POST",
                endpoint="/api/v1/paints/search",
                error=str(e),
                elapsed_time=round(elapsed_time, 3),
                exc_info=True
            )
            raise

    async def search_paints(self, query: str, environment: Optional[str] = None) -> List[Dict]:
        """Busca simples por texto (fallback)"""
        paints = await self.get_all_paints(environment=environment, limit=1000)
        query_lower = query.lower()
        filtered = []
        for paint in paints:
            if (query_lower in paint.get("name", "").lower() or
                query_lower in paint.get("color", "").lower() or
                query_lower in paint.get("surface_type", "").lower()):
                filtered.append(paint)
        return filtered[:10]
