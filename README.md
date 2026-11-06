# Python, API & LLM Reliability Rescue — Open Demo and Scoped Repairs

[![CI](https://github.com/zongsm-cmyk/llm-reliability-rescue-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/zongsm-cmyk/llm-reliability-rescue-demo/actions/workflows/ci.yml)
[![Live AWS Demo](https://img.shields.io/badge/AWS%20Lambda-Live%20API-success)](https://7hjfrxuwyxgke2h7fqhaubykda0benzq.lambda-url.us-east-1.on.aws/docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Production AI applications rarely fail due to the foundational model itself. They crash at the boundary: **malformed LLM outputs**, **pgvector latency spikes**, **database connection exhaustion during bursts**, and **unhandled 429 rate limits**.

This repository is an engineering demonstration with code and regression tests, plus links to separately scoped commercial repairs. Production behavior and financial outcomes must be verified for each engagement.

---

## What the public evidence establishes

This repository provides code, tests, and example configurations for validating structured LLM output, recovering from certain API failures, and studying PostgreSQL/pgvector behavior. The CI badge reports the status of the automated checks; it is **not** a production SLA or a customer testimonial. The public API health endpoint only indicates basic service responsiveness.

Some historical benchmark notes mention 94% latency reductions, 0% parsing failures, zero lost events, and precise p95/recall numbers. **Those claims have not been independently reproduced against a documented public workload and environment; do not treat them as verified performance results.** The relevant scripts and notes remain available for technical inspection:

- [pgvector tests and tuning examples](solutions/pgvector-latency-rescue)
- [Resilience and retry examples](solutions/resilience-shields)
- [Structured-output validator](app/validator.py)
- [Benchmark notes (workload and reproducibility review pending)](docs/benchmarks/pgvector_hnsw_rag_optimization.md)

## Need one Python, API or LLM-JSON defect repaired?

**Start with a redacted failing example and an explicit expected result.** We will assess whether the fault fits a bounded patch, agree the acceptance test, deadline and payment terms in writing, and provide a targeted fix plus regression test evidence.

- [Scoped Python/API pilot — included and excluded work](OFFER.md): the $45 illustrative pilot scope is **not** a statement that any marketplace package is priced at $45. Confirm the current listing and agreed terms before paying.
- [Askoure Systems — free 15-minute written triage](https://askoure-systems.floot.app/services/automation-rescue): more involved repairs shown at $99–$199, contingent on the agreed problem and acceptance criteria.
- [Fiverr: LLM JSON failures](https://www.fiverr.com/mhamedaskoure/fix-inconsistent-json-outputs-in-your-python-llm-api-workflow) · [Pydantic validation](https://www.fiverr.com/mhamedaskoure/add-reliable-pydantic-json-schema-validation-to-your-python-llm-workflow) · [Python / FastAPI debugging](https://www.fiverr.com/mhamedaskoure/debug-python-fastapi-llm-api-integration-errors-and-failing-requests). Marketplace conversations and payments remain inside that marketplace.

### Digital code kits (separate from custom implementation)

- [n8n Workflow Preflight Auditor](https://mhamedasskoure.gumroad.com/l/n8n-workflow-preflight-auditor)
- [LLM Reliability Rescue Kit](https://mhamedasskoure.gumroad.com/l/llm-reliability-rescue-kit)
- [Agent Runaway Guard Kit](https://mhamedasskoure.gumroad.com/l/agent-runaway-guard-kit)
- [Python/API/LLM Failover Setup](https://mhamedasskoure.gumroad.com/l/python-api-llm-failover-setup)

The linked storefronts control their own current pricing, licensing, payment and delivery policies. A listing or payment link is not proof that an order was paid, delivered, or accepted. Do not send passwords, API keys or customer records in an issue or first-contact request. **No instant delivery or uninterrupted-service guarantee is asserted.**

---

## 🛠️ Ready-to-Deploy Technical Solutions Included

### 1. pgvector HNSW Latency Rescue (`solutions/pgvector-latency-rescue/`)
- [`pgvector_optimization.sql`](solutions/pgvector-latency-rescue/pgvector_optimization.sql): Non-blocking concurrent HNSW graph builder with tuned `m=16`, `ef_construction=128`, and composite metadata covering index.
- [`asyncpg_vector_pool.py`](solutions/pgvector-latency-rescue/asyncpg_vector_pool.py): Example async connection pool and `ef_search` configuration; latency and recall must be measured on the target dataset.
- [`test_benchmark.py`](solutions/pgvector-latency-rescue/test_benchmark.py): Automated latency and recall verification harness.

### 2. Infrastructure Resilience Shields (`solutions/resilience-shields/`)
- [`celery_postgres_failover.py`](solutions/resilience-shields/celery_postgres_failover.py): Example retry/failover wrapper for selected Postgres `40P01` and provider `429` cases; safe production integration requires testing and observability.

### 3. Strict LLM Output Extraction Engine (`app/`)
- Extracts clean JSON objects even when wrapped in markdown blocks, conversational noise, or truncated responses.
- Enforces strict Pydantic v2 schemas without unsafe `eval()` or hallucinated fields.

---

## 🌐 Live AWS Lambda Proof Endpoints

Public serverless API routes for inspection. The health route alone does not verify all error paths, uptime or deployment support:
- **Interactive OpenAPI Documentation:** https://7hjfrxuwyxgke2h7fqhaubykda0benzq.lambda-url.us-east-1.on.aws/docs
- **Health Check:** https://7hjfrxuwyxgke2h7fqhaubykda0benzq.lambda-url.us-east-1.on.aws/health
- **Validation Engine:** `POST https://7hjfrxuwyxgke2h7fqhaubykda0benzq.lambda-url.us-east-1.on.aws/validate`

---

## 💻 Run tests locally; reproduce benchmarks separately

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
