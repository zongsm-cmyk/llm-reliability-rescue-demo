# Python/API Reliability — Open-Source Demo & Fixed-Scope Repair

[![CI](https://github.com/zongsm-cmyk/llm-reliability-rescue-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/zongsm-cmyk/llm-reliability-rescue-demo/actions/workflows/ci.yml)
[![AWS Example Endpoint](https://img.shields.io/badge/AWS-Example%20Endpoint-informational)](https://7hjfrxuwyxgke2h7fqhaubykda0benzq.lambda-url.us-east-1.on.aws/docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Production AI applications rarely fail due to the foundational model itself. They crash at the boundary: **malformed LLM outputs**, **pgvector latency spikes**, **database connection exhaustion during bursts**, and **unhandled 429 rate limits**.

This repository provides inspectable code examples and test resources for debugging Python/FastAPI/JSON/LLM integrations, along with links to fixed-scope paid services. It is **not** evidence of independently verified client production savings.

**Cross-platform visual walkthrough:** The [ALFAROUQWorks Instagram API/Python reliability carousel](https://www.instagram.com/alfarouqworks/p/DgGr_1HCJxd/?utm_source=github&utm_medium=readme&utm_campaign=omnichannel_repurposing_20261124&utm_content=visual_checklist) summarizes the problem for non-engineering buyers. Its comments also link back to this free GitHub demo, so interested visitors can inspect the code before considering paid resources. This is an explainer, not a substitute for the tests below.

**Fast path from a real failing case to a fix:** Start with the [strict JSON regression tests](tests/) and [reproducible duplicate-key repair](https://github.com/zongsm-cmyk/llm-reliability-rescue-demo/pull/5). If you need a ready-to-use commercial package instead of adapting the free demo, review the [Agency Tech Master Bundle on Gumroad](https://mhamedasskoure.gumroad.com/l/ktkuv?utm_source=github&utm_medium=readme&utm_campaign=omnichannel_crosslink_20261124&utm_content=top_bundle_cta) (listed here at $21.90, confirm checkout total and contents before purchasing). The open-source code remains free; purchasing is optional.

**Explore our current original developer kits:** [English product comparison](https://shop.askouresystems.com/offers/?utm_source=github&utm_medium=organic&utm_campaign=llm_demo_offers). The shop links to the individual Gumroad listings for checkout and delivery.

---

## Evidence: what this repository does and does not prove

| Area | What can be inspected | Limitations |
| --- | --- | --- |
| JSON parsing / schema validation | [FastAPI validation code](app/main.py), [strict JSON example](examples/strict_json_decoder.py) and [tests](tests/) | No independently audited real-client failure-rate claims. |
| PostgreSQL / pgvector | [Illustrative SQL and Python examples](solutions/pgvector-latency-rescue) | No raw customer dataset, controlled baseline or independently verified p95 reduction supplied here. |
| API retry / failover patterns | [Resilience examples](solutions/resilience-shields) | Example code, not a zero-data-loss or uptime guarantee. |

**Evidence policy:** Historic percentages and “zero failures” language were removed because this repository does not include the measurements needed to substantiate those outcomes. Client performance results require a comparable before/after test with sanitized logs and acceptance criteria.
---

## Proven repair example — LLM JSON corruption (13 Nov 2026)

A reproducible failure in **this public demonstration** made `POST /validate` silently accept a duplicate `company` JSON key and non-standard numeric values (including `NaN` and `1e999`). That could make an LLM/API integration accept ambiguous or non-finite data as valid.

**Fix:** route JSON extraction through the shared strict decoder; reject duplicate keys at any depth and non-finite numbers as `INVALID_JSON`, including fenced and prose-wrapped outputs. Valid outputs and the existing response format are preserved.

**Check the evidence:** [before/after patch and regression tests](https://github.com/zongsm-cmyk/llm-reliability-rescue-demo/pull/5) · [GitHub Actions CI on merged `main` (success)](https://github.com/zongsm-cmyk/llm-reliability-rescue-demo/actions/runs/43513079371). Baseline: **21 passing tests**; after repair: **98 passing tests** in the local test run, with CI green on GitHub. These are test counts, **not** a paid-client testimonial or a claim of production improvement.

**Need the same outcome for your own endpoint?** Supply one redacted failing Python/FastAPI/JSON example and an acceptance test. Discuss a **[$95 scoped repair commission](https://mhamedasskoure.gumroad.com/l/python-api-scoped-commission)** before payment, or use the [existing Fiverr Python/FastAPI service](https://www.fiverr.com/mhamedaskoure/debug-python-fastapi-llm-api-integration-errors-and-failing-requests) under that listing's actual terms. Work begins only after scope and payment terms are agreed.

---

## Choose the right reliability package (two different products)

Two separate Gumroad packages use similar names but solve different problems. **Do not confuse the prices or contents:**

| Need | Product | Regular listed price | What it covers |
| --- | --- | ---: | --- |
| Validate malformed, fenced, truncated, or schema-invalid LLM JSON in Python/FastAPI | [LLM Reliability Rescue Kit — Structured Output Validation](https://mhamedasskoure.gumroad.com/l/llm-reliability-rescue-kit?utm_source=github&utm_medium=readme&utm_campaign=omnichannel_product_clarity_20261124&utm_content=structured_output_19) | **$19** | Strict Pydantic v2 contracts, 24-case regression corpus, FastAPI endpoints, CLI, validation runbook; separate paid ZIP. |
| Handle provider outages and failed requests | [LLM Reliability Rescue Kit — Failover, Circuit Breaker & DLQ](https://mhamedasskoure.gumroad.com/l/lujvp?utm_source=github&utm_medium=readme&utm_campaign=omnichannel_product_clarity_20261124&utm_content=failover_10) | **$10** | Provider fallback, circuit breaker, SQLite dead-letter queue examples. Eligible EARLY30DEV discount may apply at checkout. |
| Pair the $10 resilience examples with the CleanQuote estimation system | [Agency Tech Master Bundle](https://mhamedasskoure.gumroad.com/l/ktkuv?utm_source=github&utm_medium=readme&utm_campaign=omnichannel_product_clarity_20261124&utm_content=bundle_2190) | **$21.90** | The bundle listing details its own contents; **do not assume it contains the separate $19 strict-validation kit**. |

All prices are product-page list prices checked on 24 Nov 2026, exclusive of any applicable taxes; checkout determines the final amount. The open-source demonstration in this repository remains free.

## 🛒 Developer Kits — Direct Gumroad Checkout

This is a free, public technical demo. Paid downloads are optional products from Askoure Tools, not prerequisites for running this repository. Review the individual listing's inclusions, license and compatibility before checkout.

| Toolkit | Current regular price | Developer promotion | Details |
| --- | ---: | ---: | --- |
| [LLM Reliability Rescue Kit](https://mhamedasskoure.gumroad.com/l/lujvp/EARLY30DEV?utm_source=github&utm_medium=organic&utm_campaign=reliability_demo_20261124) | $10.00 | **$7.00 with EARLY30DEV** | Python circuit breaker, prioritized provider fallback, SQLite dead-letter queue examples, tests and documentation. |
| [Agency Tech Master Bundle](https://mhamedasskoure.gumroad.com/l/ktkuv/EARLY30DEV?utm_source=github&utm_medium=organic&utm_campaign=reliability_demo_20261124) | $21.90 | **$15.33 with EARLY30DEV** | Bundles the LLM toolkit with the CleanQuote Estimation System and an operations manual. |
| [Automation ROI Scenario Planner](https://mhamedasskoure.gumroad.com/l/automation-roi-scenario-planner-offline/EARLY30DEV?utm_source=github&utm_medium=organic&utm_campaign=reliability_demo_20261124) | $9.00 | **$6.30 with EARLY30DEV** | Offline cost/benefit scenarios, report and pilot planning resources; ROI is not guaranteed. |
| [CleanQuote Estimation System](https://mhamedasskoure.gumroad.com/l/hblauc?utm_source=github&utm_medium=organic&utm_campaign=reliability_demo_20261124) | $14.90 | Regular price | Offline Excel estimator and editable proposal/scope templates. |

**About the coupon:** EARLY30DEV currently applies to the three listed eligible digital products (LLM kit, Agency bundle, ROI planner). It is not a store-wide code, does not apply to custom engineering services, and is not restricted to past buyers. Checkout may add applicable taxes. Confirm the final total before paying.

**Need a narrowly scoped Python/API repair?** [Request a $95 scoped engineering commission](https://mhamedasskoure.gumroad.com/l/python-api-scoped-commission?utm_source=github&utm_medium=organic&utm_campaign=reliability_demo_20261124) after agreement on scope, deliverables, acceptance test and payment terms. Do not send credentials or customer production data.

The free code in this repository remains available under its existing license; paid product files are separate and subject to their own included terms.

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
- [`test_benchmark.py`](solutions/pgvector-latency-rescue/test_benchmark.py): Synthetic-vector input test and optional latency measurement helper (no recall@k evidence).

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
