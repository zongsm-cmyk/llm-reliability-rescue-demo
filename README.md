# Production AI & Database Reliability Rescue — Live Proof & Engineering Storefront

[![CI](https://github.com/zongsm-cmyk/llm-reliability-rescue-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/zongsm-cmyk/llm-reliability-rescue-demo/actions/workflows/ci.yml)
[![Live AWS Demo](https://img.shields.io/badge/AWS%20Lambda-Live%20API-success)](https://7hjfrxuwyxgke2h7fqhaubykda0benzq.lambda-url.us-east-1.on.aws/docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Production AI applications rarely fail due to the foundational model itself. They crash at the boundary: **malformed LLM outputs**, **pgvector latency spikes**, **database connection exhaustion during bursts**, and **unhandled 429 rate limits**.

This repository serves as an open-source technical proof, benchmark suite, and commercial engineering storefront for production reliability engineering.

---

## ⚡ Verified Benchmark Evidence

All optimizations in this repository are reproducible with zero simulated smoke-and-mirrors:

| Target System / Workload | Unoptimized Baseline | Optimized Rescue Architecture | Measured Gain | Verifiable Source Code |
|:---|:---:|:---:|:---:|:---|
| **pgvector Cosine Search (1536-dim, 100k docs)** | 420.0 ms | **24.1 ms (p95)** | **94.3% Latency Drop** | [`solutions/pgvector-latency-rescue`](solutions/pgvector-latency-rescue) |
| **PostgreSQL High-Volume Query Latency** | 1,482.0 ms | **85.8 ms (p95)** | **94.2% Speedup** | [`solutions/resilience-shields`](solutions/resilience-shields) |
| **LLM Output JSON Parsing & Schema Drift** | 14.8% error rate | **0.0% Parse Failures** | **Deterministic Lock** | [`app/validator.py`](app/validator.py) |
| **Postgres Deadlocks (40P01) / 429 API Bursts** | Pipeline Crashes | **Auto-Retry & Dual Failover** | **Zero Dropped Events** | [`solutions/resilience-shields`](solutions/resilience-shields) |

---

## 🛒 Fast-Track Commercial Checkout & Instant Delivery

Need production-hardened implementations deployed directly to your staging or production cluster? We provide ready-to-run zero-touch delivery packages with guaranteed performance SLAs:

### 1. Instant Digital Packages (Immediate Code & Runbooks):
* 📦 **$9 — n8n Workflow Preflight Auditor:** Local JSON schema validation, credential node security, production preflight checklist.  
  👉 [Buy on Gumroad ($9)](https://mhamedasskoure.gumroad.com/l/n8n-workflow-preflight-auditor) | [Instant PayPal ($9)](https://paypal.me/asskoure/9)
* 🛡️ **$19 — LLM Reliability Starter Kit:** Strict Pydantic contracts, FastAPI parser, 24-case regression test corpus.  
  👉 [Buy on Gumroad ($19)](https://mhamedasskoure.gumroad.com/l/llm-reliability-rescue-kit?utm_source=github&utm_medium=readme) | [Instant PayPal ($19)](https://paypal.me/asskoure/19)
* 🤖 **$24 — Agent Runaway Guard Kit:** Anti doom-loop circuit breakers, token runaway protection, and retry-storm isolation.  
  👉 [Buy on Gumroad ($24)](https://mhamedasskoure.gumroad.com/l/agent-runaway-guard-kit) | [Instant PayPal ($24)](https://paypal.me/asskoure/24)
* 🚀 **$95 — Full Resilience & Failover Setup:** Celery retry wrappers, dead-letter deduplication, multi-provider 429 failover router.  
  👉 [Buy on Gumroad ($95)](https://mhamedasskoure.gumroad.com/l/python-api-llm-failover-setup) | [Instant PayPal ($95)](https://paypal.me/asskoure/95)
* ⚡ **$129 — PostgreSQL Query Latency Optimization:** Partial indexing DDL, query rewriting, connection pool sizing for < 100ms p95.  
  👉 [Instant PayPal ($129)](https://paypal.me/asskoure/129)
* 🛡️ **$149 — Enterprise Webhook Ingestion Engine:** HMAC verification, queue buffering, idempotent database state machines.  
  👉 [Instant PayPal ($149)](https://paypal.me/asskoure/149)
* 🎯 **$199 — Production pgvector & RAG Rescue Suite:** Concurrent HNSW indexing, asyncpg connection pooling, ef_search tuning, benchmark harness.  
  👉 [Instant PayPal ($199)](https://paypal.me/asskoure/199)

*(Direct Merchant: **MHAMED ASKOURE** | Email: `skgsm@live.fr` | Delivery SLA: Automated dispatch within 15 minutes of payment).*

---

## 📖 In-Depth Production Benchmark Guides & Runbooks
Detailed architectural breakdowns and reproducible benchmarks:
* ⚡ [PostgreSQL Query Latency Rescue: Cutting p95 Latency by 94.2% on 12.4M Rows](docs/benchmarks/postgresql_query_latency_rescue.md)
* 🎯 [pgvector HNSW Optimization: Scaling Retrieval from 420ms to 24ms under 5M Embeddings](docs/benchmarks/pgvector_hnsw_rag_optimization.md)
* 🛡️ [Zero-Loss FastAPI Webhook Ingestion Engine with <40ms ACKs](docs/benchmarks/zero_loss_webhook_ingestion_engine.md)
* ⚡ [PostgreSQL RPC Deadlock (40P01) & PostgREST 40001 Retry Storm Remediation](docs/benchmarks/supabase_rpc_concurrency_deadlock_remediation.md)

---

## 🛠️ Ready-to-Deploy Technical Solutions Included

### 1. pgvector HNSW Latency Rescue (`solutions/pgvector-latency-rescue/`)
- [`pgvector_optimization.sql`](solutions/pgvector-latency-rescue/pgvector_optimization.sql): Non-blocking concurrent HNSW graph builder with tuned `m=16`, `ef_construction=128`, and composite metadata covering index.
- [`asyncpg_vector_pool.py`](solutions/pgvector-latency-rescue/asyncpg_vector_pool.py): Production async connection pool enforcing runtime `ef_search=64` per session to guarantee 99.2% recall at 24ms.
- [`test_benchmark.py`](solutions/pgvector-latency-rescue/test_benchmark.py): Automated latency and recall verification harness.

### 2. Infrastructure Resilience Shields (`solutions/resilience-shields/`)
- [`celery_postgres_failover.py`](solutions/resilience-shields/celery_postgres_failover.py): Full idempotent wrapper handling Postgres `40P01` deadlock recovery and automatic dual-model failover on OpenAI/Anthropic `429` rate limits.

### 3. Strict LLM Output Extraction Engine (`app/`)
- Extracts clean JSON objects even when wrapped in markdown blocks, conversational noise, or truncated responses.
- Enforces strict Pydantic v2 schemas without unsafe `eval()` or hallucinated fields.

---

## 🌐 Live AWS Lambda Proof Endpoints

Verify the core parsing and validation engine running live on serverless AWS Lambda infrastructure:
- **Interactive OpenAPI Documentation:** https://7hjfrxuwyxgke2h7fqhaubykda0benzq.lambda-url.us-east-1.on.aws/docs
- **Health Check:** https://7hjfrxuwyxgke2h7fqhaubykda0benzq.lambda-url.us-east-1.on.aws/health
- **Validation Engine:** `POST https://7hjfrxuwyxgke2h7fqhaubykda0benzq.lambda-url.us-east-1.on.aws/validate`

---

## 💻 Run and Benchmark Locally

```bash
# Clone the repository
git clone https://github.com/zongsm-cmyk/llm-reliability-rescue-demo.git
cd llm-reliability-rescue-demo

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # Or on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run test suite
pytest -q

# Run Resilience & Failover Self-Test
python solutions/resilience-shields/celery_postgres_failover.py

# Start interactive local server
uvicorn app.main:app --reload
```

---

## 🤝 Custom Architecture Audits & On-Demand Implementation

Need bespoke performance tuning or an on-call engineer to resolve query bottlenecks?  
Direct inquiries & contracts: **`skgsm@live.fr`** or message on GitHub [@zongsm-cmyk](https://github.com/zongsm-cmyk).
