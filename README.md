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

## 🛒 Developer Kits — Direct Gumroad Checkout

This public repository is a free technical demonstration. For downloadable packs, review the exact included files, version, compatibility and limitations on the corresponding Gumroad page before paying. The links below lead directly to the seller's currently published listings.

| Offering | Price | What the listing provides |
| --- | ---: | --- |
| [n8n Workflow Preflight Auditor](https://mhamedasskoure.gumroad.com/l/n8n-workflow-preflight-auditor?utm_source=github&utm_medium=organic&utm_campaign=reliability_demo_readme) | **$9** | Offline checks for exported n8n JSON plus a production checklist; not an official n8n runtime validator. |
| [LLM Reliability Rescue Kit](https://mhamedasskoure.gumroad.com/l/llm-reliability-rescue-kit?utm_source=github&utm_medium=organic&utm_campaign=reliability_demo_readme) | **$19** | Python/FastAPI structured-output validation patterns and regression resources. |
| [Agent Runaway Guard Kit](https://mhamedasskoure.gumroad.com/l/agent-runaway-guard-kit?utm_source=github&utm_medium=organic&utm_campaign=reliability_demo_readme) | **$24** | Local guards for repeated tool calls, retry storms and budget limits, with engineering examples. |
| [Automation ROI Scenario Planner (offline)](https://mhamedasskoure.gumroad.com/l/automation-roi-scenario-planner-offline?utm_source=github&utm_medium=organic&utm_campaign=reliability_demo_readme) | **$9** | Offline three-scenario decision planner, CSV export, printable report and pilot brief; estimates only. |

**Need a narrowly scoped code repair?** [Python / API Bug Fix — Commission ($95 total)](https://mhamedasskoure.gumroad.com/l/python-api-scoped-commission?utm_source=github&utm_medium=organic&utm_campaign=reliability_demo_readme). The seller and buyer agree one reproducible issue, safe redacted input, deliverables and acceptance test before checkout. Gumroad charges **50% at order and 50% at completion**. The seller provides a written diagnosis, patch or documented mitigation, verification and handover within the Gumroad order. The customer applies the code changes. **No remote installation, production deployment, ongoing technical support, or guaranteed recovery time is included.**

Do not send access tokens, API keys, passwords or customer production data. The product pages and checkout terms control pricing, delivery, refunds and eligible use. There is **no site-wide discount or guaranteed 15-minute delivery promise** here; do not rely on older campaign links.

---

## 📖 In-Depth Production Benchmark Guides & Runbooks
Detailed architectural breakdowns and reproducible benchmarks:
* ⚡ [PostgreSQL Query Latency Rescue: Cutting p95 Latency by 94.2% on 12.4M Rows](docs/benchmarks/postgresql_query_latency_rescue.md)
* 🎯 [pgvector HNSW Optimization: Scaling Retrieval from 420ms to 24ms under 5M Embeddings](docs/benchmarks/pgvector_hnsw_rag_optimization.md)
* 🛡️ [Zero-Loss FastAPI Webhook Ingestion Engine with <40ms ACKs](docs/benchmarks/zero_loss_webhook_ingestion_engine.md)
* ⚡ [PostgreSQL RPC Deadlock (40P01) & PostgREST 40001 Retry Storm Remediation](docs/benchmarks/supabase_rpc_concurrency_deadlock_remediation.md)
* 🤖 [Distributed Deadline Propagation & Anti-Ghost Retry Guard for LLM Proxies](docs/benchmarks/litellm_proxy_retry_deadline_budget_propagation.md)
* 📊 [PostgreSQL & Vector DB Hosting Benchmark: Supabase vs. Neon vs. Self-Hosted](docs/benchmarks/ai_vector_db_benchmark_supabase_vs_neon.md)

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
