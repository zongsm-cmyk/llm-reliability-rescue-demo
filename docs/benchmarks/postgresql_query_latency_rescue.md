# PostgreSQL Query Latency: Reproducible Investigation and Index Test

**Document type:** Engineering method / illustrative example  
**Evidence status:** No real-client before/after measurements provided.  
**Applies to:** PostgreSQL, including managed instances where permissions permit EXPLAIN and index operations.

## Failure to investigate

A tenant-filtered query with a status predicate and a newest-first sort may scan excessive rows. Do **not** assume an index will help until you inspect the actual query plan, row counts, selectivity, and write load.

Illustrative query (table and columns must exist in the target schema):

    SELECT id, user_id, event_name, properties, created_at
    FROM events
    WHERE tenant_id = $1 AND status = 'processed'
    ORDER BY created_at DESC
    LIMIT 50;

## Before measurement

1. Capture the exact query, bind values, PostgreSQL version, table cardinality, indexes and row estimates.
2. Run EXPLAIN (ANALYZE, BUFFERS) in an authorized nonproduction replica with representative data. Beware that ANALYZE actually executes the query; for writes, use an appropriate rollback and read permissions.
3. Record p50/p95/p99 over representative repeated requests, peak concurrency, buffer reads/hits, CPU, query plan and cache warm-up procedure.
4. Confirm whether the observed bottleneck is filtering, sorting, joins, lock waiting, storage I/O, or connection exhaustion.

## Candidate intervention (illustrative, NOT a universal fix)

    CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_tenant_processed_created
      ON events (tenant_id, created_at DESC)
      WHERE status = 'processed';

Run this **outside** a transaction block, only after evaluating additional disk space and index/write overhead. This index is tailored to the stated WHERE/ORDER BY combination; it does not promise an index-only scan because the query also selects columns not included in the index.

Do not indiscriminately INCLUDE large JSONB payload columns or increase work_mem/autovacuum settings without workload evidence. Test optional changes one at a time.

## After measurement and rollback

Repeat the same query mix with matched input distribution, warm-up, environment and concurrency. Save query plans and raw timings. The gain is measured, not inferred.

| Metric | Before | After | Evidence |
| --- | --- | --- | --- |
| p95 response time | not measured here | not measured here | raw samples |
| Buffer reads/hits | not measured here | not measured here | EXPLAIN buffers |
| CPU / connection waits | not measured here | not measured here | instance telemetry |
| Write overhead / index size | not measured here | not measured here | catalog stats |

If the candidate fails acceptance criteria, evaluate a controlled index removal:

    DROP INDEX CONCURRENTLY IF EXISTS idx_events_tenant_processed_created;

Do not execute deployment SQL against a client's system without its authorization and a rollback/maintenance plan. This file is an example, not production certification.


---

## Evidence and purchasing boundaries

This document is an engineering method and sample, **not measured customer production results**. No customer data, deployment logs, before/after latency records, or independently verified ROI metrics are supplied here. Validate changes on your own staging workload and capture the measured before/after evidence before claiming a gain.

For a separate **single, reproducible Python/API code bug**, the published [Gumroad fixed-scope Commission ($95)](https://mhamedasskoure.gumroad.com/l/python-api-scoped-commission) is available after a free written scope check. It is **not** a general infrastructure deployment or an always-on operations service. No payment claim, no guarantee of zero downtime.