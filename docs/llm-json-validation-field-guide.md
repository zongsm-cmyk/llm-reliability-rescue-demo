# LLM JSON fails in FastAPI: a five-case validation checklist

A model can return syntactically valid JSON that still breaks a backend: numbers arrive as strings, required fields disappear, untrusted prose surrounds the object, or two candidate objects appear. These are **different failures**, and handling them as one generic exception hides the actual fix.

This free, reproducible guide uses the [LLM Reliability Rescue public demo](../README.md). It makes **no paid API requests** and does not claim any customer's results.

## Reproduce locally

From the repository root, install the existing demo requirements and start its FastAPI server:

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open a **second** terminal and run the following with Python 3. The script sends harmless fictional example data to the local `/validate` endpoint:

```python
import json
from urllib.request import Request, urlopen

url = "http://127.0.0.1:8000/validate"
good = {
    "company": "Example Studio",
    "fit_score": 87,
    "summary": "Example-only lead assessment.",
    "risks": ["Demo risk"],
    "next_action": "Review the fictional record.",
}

cases = [
    ("valid_object", json.dumps(good), True, None),
    ("fenced_object", "```json\n" + json.dumps(good) + "\n```", True, None),
    ("string_instead_of_int", json.dumps({**good, "fit_score": "87"}), False, "SCHEMA_VALIDATION_FAILED"),
    ("two_objects", json.dumps(good) + "\n" + json.dumps(good), False, "AMBIGUOUS_JSON"),
    ("broken_json", '{"company":', False, "INVALID_JSON"),
]

for name, raw, expected_ok, expected_code in cases:
    request = Request(
        url,
        data=json.dumps({"raw": raw}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=10) as response:
        result = json.load(response)

    code = (result.get("error") or {}).get("code")
    passed = result.get("ok") is expected_ok and code == expected_code
    print(f"{name}: {'PASS' if passed else 'FAIL'} (ok={result.get('ok')}, code={code})")
    if not passed:
        raise SystemExit(f"Unexpected validation behavior: {name}")
```

If the local server is running with the code in this repository, the five cases should report `PASS`.

## What each outcome actually tells you

| Result | Meaning | Safer next action |
|---|---|---|
| `ok: true` | Exactly one object met the strict `LeadAnalysis` schema. | Use the validated `data`, not the original raw output. |
| `SCHEMA_VALIDATION_FAILED` | JSON parsed, but field types, constraints or required fields do not match. | Review the reported safe field locations; avoid silent string-to-number coercion. |
| `AMBIGUOUS_JSON` | More than one valid object was found in the raw response. | Refuse to guess; request one unambiguous object. |
| `INVALID_JSON` | No suitable single JSON object was extractable without inventing information. | Handle the failure explicitly and bound any retry. |

**Important:** The demo intentionally responds with HTTP 200 for schema/JSON failures and reports the failure in the response body. Client code must check `ok`; a successful HTTP response **does not** mean valid model data.

## Review before production use

- Enforce the exact schema your application actually needs; the demo's lead-analysis model is only an example.
- Set reasonable request-size and retry budgets; retries should not silently amplify cost.
- Keep raw model output untrusted; never `eval` it or use its values in privileged commands without separate authorization.
- Regression-test malformed output, multiple objects, extra keys, missing required keys, and numeric strings.
- Validate authentication, rate limiting, logging/privacy controls, and error handling before treating any proof application as production ready.

**Need a larger, packaged implementation?** The separately sold [LLM Reliability Rescue Kit ($19)](https://mhamedasskoure.gumroad.com/l/llm-reliability-rescue-kit?utm_source=github&utm_medium=organic&utm_campaign=winner_validation_20261025&utm_content=llm_json_field_guide) includes integration guidance, a regression corpus, CI examples, and runbooks. The public demonstration above remains free. The paid kit does not provide an LLM model or paid API access.
