from __future__ import annotations

import json
from json import JSONDecodeError
from typing import Any, Literal

from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel, ConfigDict, Field, ValidationError

app = FastAPI(
    title="LLM Reliability Rescue Proof",
    version="1.1.0",
    description="Proof of robust JSON extraction and schema validation.",
)

class LeadAnalysis(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    company: str = Field(min_length=1, max_length=200)
    fit_score: int = Field(ge=0, le=100)
    summary: str = Field(min_length=1, max_length=2000)
    risks: list[str] = Field(default_factory=list, max_length=20)
    next_action: str = Field(min_length=1, max_length=1000)

class RawLLMOutput(BaseModel):
    raw: str = Field(min_length=1, max_length=100_000)

class SafeError(BaseModel):
    code: Literal["INVALID_JSON", "AMBIGUOUS_JSON", "SCHEMA_VALIDATION_FAILED"]
    message: str
    details: list[dict[str, Any]] = Field(default_factory=list)

class ValidationResponse(BaseModel):
    ok: bool
    data: LeadAnalysis | None = None
    error: SafeError | None = None

def _strip_single_json_fence(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    if len(lines) >= 3 and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()
    return stripped

def _balanced_object_candidates(text: str):
    depth = 0
    start: int | None = None
    in_string = False
    escaped = False
    for index, char in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
            continue
        if char == "{":
            if depth == 0:
                start = index
            depth += 1
        elif char == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None:
                yield text[start:index + 1]
                start = None

def parse_json_object(raw: str) -> dict[str, Any]:
    text = _strip_single_json_fence(raw)
    try:
        parsed = json.loads(text)
    except JSONDecodeError:
        parsed = None
    else:
        if isinstance(parsed, dict):
            return parsed
        raise ValueError("Top-level JSON must be an object.")

    valid_objects: list[dict[str, Any]] = []
    for candidate in _balanced_object_candidates(text):
        try:
            parsed = json.loads(candidate)
        except JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            valid_objects.append(parsed)

    if len(valid_objects) == 1:
        return valid_objects[0]
    if len(valid_objects) > 1:
        raise ValueError("Multiple valid JSON objects found; refusing to choose one.")

    raise ValueError("No valid JSON object could be extracted without inventing data.")

def _safe_validation_details(exc: ValidationError) -> list[dict[str, Any]]:
    safe = []
    for item in exc.errors(include_url=False, include_context=False, include_input=False):
        safe.append({
            "type": item.get("type", "validation_error"),
            "loc": [str(part) for part in item.get("loc", ())],
            "msg": item.get("msg", "Invalid value"),
        })
    return safe

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/validate", response_model=ValidationResponse)
def validate_output(payload: RawLLMOutput) -> ValidationResponse:
    try:
        parsed = parse_json_object(payload.raw)
    except ValueError as exc:
        ambiguous = str(exc).startswith("Multiple valid JSON objects")
        return ValidationResponse(
            ok=False,
            error=SafeError(
                code="AMBIGUOUS_JSON" if ambiguous else "INVALID_JSON",
                message=(
                    "Multiple valid JSON objects were found; the service will not choose one."
                    if ambiguous
                    else "The output does not contain a valid JSON object."
                ),
            ),
        )

    try:
        validated = LeadAnalysis.model_validate(parsed)
    except ValidationError as exc:
        return ValidationResponse(
            ok=False,
            error=SafeError(
                code="SCHEMA_VALIDATION_FAILED",
                message="JSON was extracted but does not satisfy the required schema.",
                details=_safe_validation_details(exc),
            ),
        )

    return ValidationResponse(ok=True, data=validated)

handler = Mangum(app)
