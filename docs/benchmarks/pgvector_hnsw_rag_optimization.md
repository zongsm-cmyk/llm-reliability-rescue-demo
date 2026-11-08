# pgvector HNSW: Index Tuning and Recall/Latency Measurement Guide

**Document type:** Reproducible engineering guide, not a completed independent benchmark.  
**Evidence status:** No 5-million-vector dataset, raw recall labels, query logs or before/after measurements are supplied here.

## The real trade-off

Approximate nearest-neighbor search requires measuring both **latency** and **recall**. A low p95 number without recall@k against an exact-search reference does not prove quality. Tenant filters, post-filtering and HNSW search settings can substantially change outcomes.

## Sample index plan

Adapt these examples only after inspecting your schema, extension version, memory and workload. Run CREATE INDEX CONCURRENTLY outside transaction blocks.

    CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_document_embeddings_hnsw_cosine
      ON document_embeddings USING hnsw (embedding vector_cosine_ops)
      WITH (m = 16, ef_construction = 128)
      WHERE is_active = true AND deleted_at IS NULL;

A query intended to use that partial index must include compatible active/deleted predicates. Adjust index choices and HNSW parameters based on real vector distribution. For session-level comparison, test multiple settings such as:

    SET hnsw.ef_search = 64;

This is a candidate configuration, **not** proof of a specific latency or recall result.

## Verification procedure

1. Define corpus size, dimensions, pgvector/Postgres versions, hardware, filters, top_k and an agreed recall target.
2. Sample representative query embeddings. Compare ANN neighbors with an exact-search reference under a controlled procedure.
3. Measure p50/p95/p99, recall@k, query throughput, index build time, index size and connection pooling under equivalent load.
4. Compare candidates fairly, including tenant filtering and cold/warm caches.
5. Retain raw timing files, recall labels and EXPLAIN plans, then publish numerical claims only if the data supports them.

Existing **illustrative code**, not a measured acceptance certificate:
- [HNSW SQL candidate](../../solutions/pgvector-latency-rescue/pgvector_optimization.sql)
- [asyncpg example](../../solutions/pgvector-latency-rescue/asyncpg_vector_pool.py)
- [synthetic-vector test/benchmark helper](../../solutions/pgvector-latency-rescue/test_benchmark.py)

The sample helper generates random vectors; it does not provide a real-client corpus or a reproducible recall@k ground truth.

| Metric | Baseline | Candidate | Measurement record |
| --- | --- | --- | --- |
| p95 latency | pending | pending | raw samples |
| recall@k | pending | pending | exact-search reference |
| index size/build time | pending | pending | database telemetry |
| write/read contention | pending | pending | representative load |

No fixed percentage improvement or sub-25ms outcome is claimed.


---

## Evidence and purchasing boundaries

This document is an engineering method and sample, **not measured customer production results**. No customer data, deployment logs, before/after latency records, or independently verified ROI metrics are supplied here. Validate changes on your own staging workload and capture the measured before/after evidence before claiming a gain.

For a separate **single, reproducible Python/API code bug**, the published [Gumroad fixed-scope Commission ($95)](https://mhamedasskoure.gumroad.com/l/python-api-scoped-commission) is available after a free written scope check. It is **not** a general infrastructure deployment or an always-on operations service. No payment claim, no guarantee of zero downtime.