# Python/API Reliability — Open-Source Demo & Fixed-Scope Repair

[![CI](https://github.com/zongsm-cmyk/llm-reliability-rescue-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/zongsm-cmyk/llm-reliability-rescue-demo/actions/workflows/ci.yml)
[![AWS Example Endpoint](https://img.shields.io/badge/AWS-Example%20Endpoint-informational)](https://7hjfrxuwyxgke2h7fqhaubykda0benzq.lambda-url.us-east-1.on.aws/docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Production AI applications rarely fail due to the foundational model itself. They crash at the boundary: **malformed LLM outputs**, **pgvector latency spikes**, **database connection exhaustion during bursts**, and **unhandled 429 rate limits**.

This repository provides inspectable code examples and test resources for debugging Python/FastAPI/JSON/LLM integrations, along with links to fixed-scope paid services. It is **not** evidence of independently verified client production savings.

---

## Evidence: what this repository does and does not prove

| Area | What can be inspected | Limitations |
| --- | --- | --- |
| JSON parsing / schema validation | [FastAPI validation code](app/main.py), [strict JSON example](examples/strict_json_decoder.py) and [tests](tests/) | No independently audited real-client failure-rate claims. |
| PostgreSQL / pgvector | [Illustrative SQL and Python examples](solutions/pgvector-latency-rescue) | No raw customer dataset, controlled baseline or independently verified p95 reduction supplied here. |
| API retry / failover patterns | [Resilience examples](solutions/resilience-shields) | Example code, not a zero-data-loss or uptime guarantee. |

**Evidence policy:** Historic percentages and “zero failures” language were removed because this repository does not include the measurements needed to substantiate those outcomes. Client performance results require a comparable before/after test with sanitized logs and acceptance criteria.
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

## 📖 Reproducible Engineering Methods & Test Plans
These are code examples and measurement procedures, **not independently verified production benchmark results**:
* [PostgreSQL Query Latency — illustrative method and design notes](docs/benchmarks/postgresql_query_latency_rescue.md)
* [pgvector HNSW Optimization — method and tuning discussion](docs/benchmarks/pgvector_hnsw_rag_optimization.md)
* [FastAPI Webhook Ingestion — reliability patterns and test considerations](docs/benchmarks/zero_loss_webhook_ingestion_engine.md)
* ⚡ [PostgreSQL RPC Deadlock (40P01) & PostgREST 40001 Retry Storm Remediation](docs/benchmarks/supabase_rpc_concurrency_deadlock_remediation.md)
* 🤖 [Distributed Deadline Propagation & Anti-Ghost Retry Guard for LLM Proxies](docs/benchmarks/litellm_proxy_retry_deadline_budget_propagation.md)
* 📊 [PostgreSQL & Vector DB Hosting Benchmark: Supabase vs. Neon vs. Self-Hosted](docs/benchmarks/ai_vector_db_benchmark_supabase_vs_neon.md)

---

## 🛠️ Reference Implementations and Examples Included

### 1. pgvector HNSW Latency Rescue (`solutions/pgvector-latency-rescue/`)
- [`pgvector_optimization.sql`](solutions/pgvector-latency-rescue/pgvector_optimization.sql): Example HNSW index and metadata-index settings to test against a real workload before adopting.
- [`asyncpg_vector_pool.py`](solutions/pgvector-latency-rescue/asyncpg_vector_pool.py): Async connection-pool and search-setting example. Recall and latency must be measured on the target workload.
- [`test_benchmark.py`](solutions/pgvector-latency-rescue/test_benchmark.py): Automated latency and recall verification harness.

### 2. Infrastructure Resilience Shields (`solutions/resilience-shields/`)
- [`celery_postgres_failover.py`](solutions/resilience-shields/celery_postgres_failover.py): Example retry/failover handling for PostgreSQL `40P01` and LLM API `429`; test and adapt before production use.

### 3. Strict LLM Output Extraction Engine (`app/`)
- Extracts one unambiguous valid JSON object from Markdown fences or wrapper prose; rejects malformed or truncated JSON without inventing data.
- Enforces strict Pydantic v2 schemas without unsafe `eval()` or hallucinated fields.

---

## 🌐 Optional AWS Lambda Demo Endpoints

These URLs are provided for inspection when available; their uptime and current deployment status have not been verified as part of this README update:
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

## 🤝 Paid, Fixed-Scope Help

**One reproducible Python/FastAPI/API issue:** [$95 Gumroad Commission](https://mhamedasskoure.gumroad.com/l/python-api-scoped-commission) — 50% deposit at checkout after written scope agreement; patch/mitigation, regression check and handover delivered within the order. No remote installation or production access.

**Up to three slow PostgreSQL queries:** [Written $300 audit offer](https://github.com/zongsm-cmyk/postgresql-query-optimization-benchmark) — agreed milestone and sanitized EXPLAIN evidence before starting.

**Ask for a scope check:** [zongsm@gmail.com](mailto:zongsm@gmail.com?subject=Scoped%20Python%20or%20PostgreSQL%20Repair) or message [@zongsm-cmyk](https://github.com/zongsm-cmyk). Do not send secrets, production data or credentials. These are offers, not a claim that a client has purchased or paid.
