# Supabase vs Neon vs Self-Hosted PostgreSQL for RAG — Evaluation Worksheet

**Document type:** Vendor-neutral comparison framework.  
**Evidence status:** This repository does **not** include raw cross-provider benchmark runs or validated current vendor pricing.

## What to compare

The same schema and request mix can behave differently across managed database platforms because compute size, connection pooling, cold starts, network location, storage performance, tenancy and workload limits differ. Never publish a price or latency winner without a dated vendor quote and controlled measurements.

| Decision factor | Supabase | Neon | Self-hosted |
| --- | --- | --- | --- |
| Authentication and integrated platform features | evaluate project needs | evaluate app needs | design and maintain yourself |
| Branching / environment isolation | verify current plan | verify current plan | design backups and branching |
| Pooling and concurrent connections | test actual endpoint | test actual endpoint | configure and operate |
| pgvector version and index features | verify extension | verify extension | verify installed extension |
| Cold start and p95 under load | measure | measure | measure |
| Backups, HA and incident response | verify service terms | verify service terms | operator responsibility |
| Total monthly cost, including egress | obtain current quote | obtain current quote | include labor and hosting |

## Controlled benchmark design

1. Record the same PostgreSQL/pgvector versions where possible, fixed instance size and connection limits.
2. Generate a fixed synthetic dataset with known seed, embedding dimension, tenant mix, query set and ground-truth neighbor labels. Synthetic results are not customer production claims.
3. Run warm and cold trials, stable concurrency and a known client region for each candidate.
4. Capture p50/p95/p99 for inserts and vector searches, recall@k, index build time, connection errors and actual billed resource consumption.
5. Save full raw samples and config; only then compare price/performance.

**Do not interpret differences caused by dissimilar compute tiers as intrinsic differences between providers.**

A practical [pgvector indexing guide](pgvector_hnsw_rag_optimization.md) and [SQL examples](../../solutions/pgvector-latency-rescue/pgvector_optimization.sql) are provided separately.

## What this page does not establish

No historical statement that we ran a 100,000-query comparison, achieved a 94% latency reduction, or stress-tested these vendors in client production is evidenced by the repository. We therefore make **none** of those claims, and we do not assert affiliate eligibility or commission amounts.


---

## Evidence and purchasing boundaries

This document is an engineering method and sample, **not measured customer production results**. No customer data, deployment logs, before/after latency records, or independently verified ROI metrics are supplied here. Validate changes on your own staging workload and capture the measured before/after evidence before claiming a gain.

For a separate **single, reproducible Python/API code bug**, the published [Gumroad fixed-scope Commission ($95)](https://mhamedasskoure.gumroad.com/l/python-api-scoped-commission) is available after a free written scope check. It is **not** a general infrastructure deployment or an always-on operations service. No payment claim, no guarantee of zero downtime.