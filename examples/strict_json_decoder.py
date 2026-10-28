"""Strict, privacy-safe JSON decoder for reliability-sensitive client integrations.

Standalone example: does not alter the deployed FastAPI endpoint.
"""
from __future__ import annotations

import json
from typing import Any


class DuplicateKeyError(ValueError):
    """Repeated object member would otherwise overwrite client data."""


class NonFiniteNumberError(ValueError):
    """JSON extension for NaN/Infinity is not interoperable."""


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name, value in pairs:
        if name in result:
            raise DuplicateKeyError("Duplicate JSON object key")
        result[name] = value
    return result


def _finite_only(token: str) -> Any:
    raise NonFiniteNumberError("Non-finite JSON number")


def strict_loads(raw: str) -> Any:
    """Decode JSON without silent key overrides or non-standard numeric values."""
    return json.loads(raw, object_pairs_hook=_unique_pairs, parse_constant=_finite_only)
