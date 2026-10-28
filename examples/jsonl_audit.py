"""Offline JSONL audit: python -m examples.jsonl_audit < input.jsonl > report.jsonl.

One physical line per record. No raw data is ever copied to the report.
Exit 0 if all accepted, 1 if any rejected; no network or paid API use.
"""
import json
import sys
from pydantic import ValidationError
from app.main import RawLLMOutput, validate_output


def check(raw, number):
    try:
        data = RawLLMOutput(raw=raw.rstrip("\r\n"))
    except ValidationError:
        return {"line": number, "ok": False, "code": "INVALID_INPUT"}
    response = validate_output(data)
    if response.ok:
        return {"line": number, "ok": True, "fit_score": response.data.fit_score}
    return {"line": number, "ok": False, "code": response.error.code}


def run(source, dest):
    count = failed = 0
    for count, line in enumerate(source, 1):
        result = check(line, count)
        dest.write(json.dumps(result, separators=(",", ":")) + "\n")
        failed += not result["ok"]
    return count, failed


if __name__ == "__main__":
    total, rejected = run(sys.stdin, sys.stdout)
    print(f"records={total} rejected={rejected}", file=sys.stderr)
    raise SystemExit(1 if rejected else 0)
