"""Synthetic vector helper and optional workload-specific latency measurement.

This file does NOT claim the test includes a real dataset, exact-neighbor ground
truth, or measured customer production results.
"""
from __future__ import annotations

import time
from typing import Any
import numpy as np


def generate_mock_embedding(dim: int = 1536, seed: int | None = None) -> list[float]:
    """Generate a reproducible unit vector for test *inputs* only."""
    if dim < 1:
        raise ValueError("dim must be positive")
    rng = np.random.default_rng(seed)
    vector = rng.standard_normal(dim).astype(np.float32)
    return (vector / np.linalg.norm(vector)).tolist()


def test_mock_vector_embedding_generation():
    """Checks basic synthetic-input properties; not pgvector performance."""
    vector = generate_mock_embedding(dim=1536, seed=42)
    assert len(vector) == 1536
    assert abs(float(np.linalg.norm(vector)) - 1.0) < 1e-4
    assert vector == generate_mock_embedding(dim=1536, seed=42)


async def run_latency_benchmark(
    pool: Any, tenant_id: str, sample_queries: int = 100, *, seed: int = 42
) -> dict[str, float]:
    """Measure client-observed times for a caller-supplied configured pool.

    Results depend on database, network, dataset, load and cache. This does not
    measure recall@k, and intentionally asserts no invented universal SLA.
    """
    if sample_queries < 1:
        raise ValueError("sample_queries must be >= 1")
    rng = np.random.default_rng(seed)
    latencies: list[float] = []
    for _ in range(sample_queries):
        vec = rng.standard_normal(1536).astype(np.float32)
        vec = (vec / np.linalg.norm(vec)).tolist()
        started = time.perf_counter()
        await pool.similarity_search(tenant_id, vec, top_k=5)
        latencies.append((time.perf_counter() - started) * 1000.0)
    return {
        "n": float(sample_queries),
        "p50_ms": float(np.percentile(latencies, 50)),
        "p95_ms": float(np.percentile(latencies, 95)),
        "p99_ms": float(np.percentile(latencies, 99)),
    }


if __name__ == "__main__":
    print("Import run_latency_benchmark and supply an authorized initialized Postgres pool.")
    print("Do not infer recall, performance guarantees or production savings from synthetic vectors.")
