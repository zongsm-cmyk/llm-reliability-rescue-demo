# LLM Reliability Rescue — Live Proof

This repository is a compact proof of a production problem: LLM output often looks correct until malformed JSON, schema drift, coercion, or wrapper text breaks an application.

The demo uses **no paid LLM API**. It focuses on the reliability layer around model output.

## What this proves
- Extract a valid JSON object from plain JSON, fenced JSON, or surrounding prose.
- Never use `eval` or invent missing data.
- Validate with strict Pydantic v2 types and constraints.
- Return explicit, structured failures.
- Lock behavior with regression tests.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API.
## Example

Send a string that contains model-like output to `POST /validate`. The service extracts a JSON object only when it is actually parseable, then applies a strict schema.

Example valid object:

```json
{
  "company": "Acme Labs",
  "fit_score": 87,
  "summary": "Strong API fit.",
  "risks": ["Small engineering team"],
  "next_action": "Book a technical discovery call."
}
```

A valid payload returns `ok: true`. Invalid JSON or schema violations return `ok: false` with a safe error code and validation details.

## Test

```bash
pytest -q
```
## AWS-ready shape

`app.main:handler` exposes a Mangum adapter so the same FastAPI app can be packaged for AWS Lambda/API Gateway or a Lambda Function URL.

## Commercial scope

This proof demonstrates the same class of work as the fixed-scope **AI / LLM Reliability Rescue** starter in [OFFER.md](OFFER.md): reproduce one failing output step, add parsing/validation/failure handling, and return a patch plus regression test.

No performance claims, customer history, or paid-client results are implied by this repository.

## Live AWS proof

- Health: https://7hjfrxuwyxgke2h7fqhaubykda0benzq.lambda-url.us-east-1.on.aws/health
- Interactive docs: https://7hjfrxuwyxgke2h7fqhaubykda0benzq.lambda-url.us-east-1.on.aws/docs
- Validation endpoint: https://7hjfrxuwyxgke2h7fqhaubykda0benzq.lambda-url.us-east-1.on.aws/validate

The public demo is deliberately resource-capped on AWS Lambda: 256 MB memory, 5-second timeout, and reserved concurrency of 1. It is a proof endpoint, not a production SLA.
