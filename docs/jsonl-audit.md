# Offline JSONL audit (no external APIs)

Run from the repository root after installing requirements:

```bash
python -m examples.jsonl_audit < responses.jsonl > audit.jsonl
```

Each **physical input line** is one raw LLM response. JSON strings containing line breaks must encode them as `\\n`; multi-line records are not supported. For each line, the CLI applies the same strict schema and ambiguity policy as `POST /validate`.

Output includes only line index, acceptance status, optional numeric score or safe error code; it never echoes customer input. A successful audit exits 0; any invalid record exits 1. The count is printed to stderr. Redirect stdout to a new file to avoid overwriting the input. There is no paid-model call or network dependency.

Limitations: The CLI uses standard stream redirection, so output is not atomically persisted. It is a local preflight tool, not proof of production deployment or paid acceptance.
