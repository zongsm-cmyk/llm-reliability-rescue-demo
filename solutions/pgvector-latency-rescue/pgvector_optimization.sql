-- PGVECTOR HNSW INDEX CANDIDATE — ILLUSTRATIVE ONLY
--
-- No published dataset/latency/recall evidence is bundled with this repository.
-- Confirm the schema, extension version, permissions and maintenance window.
-- CREATE INDEX CONCURRENTLY must run outside a transaction block.
-- Do not apply automatically to a production database.

-- Example for a table with:
-- document_embeddings(embedding vector(1536), tenant_id, document_id,
--                     created_at, chunk_index, token_count, is_active, deleted_at)

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_document_embeddings_hnsw_cosine
ON document_embeddings USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 128)
WHERE is_active = true AND deleted_at IS NULL;

-- Optional tenant metadata index; assess actual query plans and write overhead.
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_embeddings_metadata_covering
ON document_embeddings (tenant_id, document_id, created_at DESC)
INCLUDE (chunk_index, token_count)
WHERE is_active = true;

-- Session-level search parameter candidate; tune to your measured recall@k.
-- SET hnsw.ef_search = 64;
--
-- Measure ANN latency AND recall vs exact neighbors with the same filters.
-- No '94% faster', '24ms p95' or '99% recall' results are claimed here.

-- Controlled rollback examples; also require an appropriate maintenance plan:
-- DROP INDEX CONCURRENTLY IF EXISTS idx_document_embeddings_hnsw_cosine;
-- DROP INDEX CONCURRENTLY IF EXISTS idx_embeddings_metadata_covering;
