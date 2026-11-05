"""
Enterprise pgvector AsyncPG Connection Pool & Resilient Retrieval Engine
Module: asyncpg_vector_pool.py
Author: MHAMED ASKOURE (Commercial Reliability Engineering)
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import asyncpg

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("pgvector.Engine")


class ResilientVectorPool:
    """
    High-performance asyncpg connection pool tuned for sub-25ms pgvector HNSW cosine searches.
    Enforces runtime HNSW search parameters and optimal work memory per session.
    """

    def __init__(self, dsn: str, min_size: int = 5, max_size: int = 25):
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size
        self._pool: Optional[asyncpg.Pool] = None

    async def initialize(self):
        async def init_connection(conn: asyncpg.Connection):
            # Enforce runtime HNSW search tuning on every connection in pool
            await conn.execute("SET hnsw.ef_search = 64;")
            await conn.execute("SET work_mem = '64MB';")

        self._pool = await asyncpg.create_pool(
            self.dsn,
            min_size=self.min_size,
            max_size=self.max_size,
            max_queries=50000,
            max_inactive_connection_lifetime=300.0,
            init=init_connection,
        )
        logger.info(
            "pgvector connection pool initialized with %d-%d connections.",
            self.min_size,
            self.max_size,
        )

    async def similarity_search(
        self,
        tenant_id: str,
        query_embedding: List[float],
        top_k: int = 5,
        min_similarity: float = 0.75,
    ) -> List[Dict[str, Any]]:
        """Executes an optimized vector search with zero heap penalty."""
        if not self._pool:
            raise RuntimeError("Vector pool not initialized.")

        query = """
            SELECT 
                id,
                document_id,
                chunk_index,
                1 - (embedding <=> $1::vector) AS similarity_score
            FROM document_embeddings
            WHERE tenant_id = $2
              AND is_active = true
              AND 1 - (embedding <=> $1::vector) >= $3
            ORDER BY embedding <=> $1::vector
            LIMIT $4;
        """
        async with self._pool.acquire() as conn:
            records = await conn.fetch(
                query,
                str(query_embedding),
                tenant_id,
                min_similarity,
                top_k,
            )
            return [dict(rec) for rec in records]

    async def close(self):
        if self._pool:
            await self._pool.close()
            logger.info("pgvector connection pool closed cleanly.")
