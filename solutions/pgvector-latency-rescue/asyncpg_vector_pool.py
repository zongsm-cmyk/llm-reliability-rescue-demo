"""Illustrative pgvector/asyncpg pool and cosine-distance query.

Requires a PostgreSQL schema with the documented columns, pgvector extension and
an authorized DSN. Not a benchmark or a latency/SLA guarantee.
"""
from __future__ import annotations

import logging
from typing import Any
import asyncpg

logger = logging.getLogger(__name__)


class ResilientVectorPool:
    """Small configurable connection pool; tune per server capacity."""

    def __init__(self, dsn: str, min_size: int = 1, max_size: int = 5):
        if min_size < 1 or max_size < min_size:
            raise ValueError("Expected 1 <= min_size <= max_size")
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size
        self._pool: asyncpg.Pool | None = None

    async def initialize(self) -> None:
        async def init_connection(conn: asyncpg.Connection) -> None:
            # Candidate tuning value only. Benchmark for recall and latency.
            await conn.execute("SET hnsw.ef_search = 64")

        self._pool = await asyncpg.create_pool(
            dsn=self.dsn,
            min_size=self.min_size,
            max_size=self.max_size,
            init=init_connection,
        )

    async def similarity_search(
        self,
        tenant_id: str,
        query_embedding: list[float],
        top_k: int = 5,
        min_similarity: float = 0.75,
    ) -> list[dict[str, Any]]:
        """Return scored example records; no claim of an index-only scan."""
        if self._pool is None:
            raise RuntimeError("Initialize the pool first")
        if top_k < 1 or top_k > 1000:
            raise ValueError("top_k must be between 1 and 1000")
        if not 0.0 <= min_similarity <= 1.0:
            raise ValueError("min_similarity must be in [0, 1]")
        if not query_embedding:
            raise ValueError("embedding cannot be empty")
        # Casting the vector parameter is explicit; don't concatenate SQL.
        query = """
            SELECT id, document_id, chunk_index,
                   1 - (embedding <=> $1::vector) AS similarity_score
            FROM document_embeddings
            WHERE tenant_id = $2
              AND is_active = true
              AND deleted_at IS NULL
              AND 1 - (embedding <=> $1::vector) >= $3
            ORDER BY embedding <=> $1::vector
            LIMIT $4
        """
        async with self._pool.acquire() as conn:
            records = await conn.fetch(
                query, str(query_embedding), tenant_id, min_similarity, top_k
            )
        return [dict(record) for record in records]

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None
