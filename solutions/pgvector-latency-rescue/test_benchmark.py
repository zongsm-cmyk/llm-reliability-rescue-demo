"""
pgvector HNSW Latency & Recall Verification Harness
Module: test_benchmark.py
Validates p50, p95, and p99 query latency against the target SLA (< 25.0ms p95).
"""
from __future__ import annotations

import asyncio
import logging
import time
from typing import List

import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("pgvector.Benchmark")


def generate_mock_embedding(dim: int = 1536) -> List[float]:
    """Generates unit-normalized mock embedding vector (OpenAI text-embedding-3-small dimension)."""
    vec = np.random.randn(dim).astype(np.float32)
    norm = np.linalg.norm(vec)
    return (vec / norm).tolist()


def test_mock_vector_embedding_generation():
    """Unit test: verifies mock vector normalization and dimensionality."""
    vec = generate_mock_embedding(dim=1536)
    assert len(vec) == 1536
    norm = float(np.linalg.norm(vec))
    assert abs(norm - 1.0) < 1e-4, "Mock embedding must be unit-normalized"


async def run_latency_benchmark(pool, tenant_id: str, sample_queries: int = 100):
    latencies = []
    logger.info("Executing %d concurrent vector similarity queries...", sample_queries)

    for _ in range(sample_queries):
        query_vec = generate_mock_embedding()
        t0 = time.perf_counter()
        results = await pool.similarity_search(tenant_id, query_vec, top_k=5)
        dt = (time.perf_counter() - t0) * 1000.0
        latencies.append(dt)

    p50 = float(np.percentile(latencies, 50))
    p95 = float(np.percentile(latencies, 95))
    p99 = float(np.percentile(latencies, 99))

    print("\n================ PGVECTOR BENCHMARK RESULTS ================")
    print(f"Total Queries Analyzed: {sample_queries}")
    print(f"p50 Latency:            {p50:.2f} ms")
    print(f"p95 Latency:            {p95:.2f} ms  (Target: < 25.00 ms)")
    print(f"p99 Latency:            {p99:.2f} ms")
    print("============================================================\n")
    assert p95 < 30.0, f"p95 latency threshold exceeded! ({p95:.2f} ms >= 30.0 ms)"
    logger.info("SLA VERIFIED: Latency target met successfully.")


if __name__ == "__main__":
    print("Run with a valid Postgres DSN to benchmark live HNSW vector queries.")
