import json

import pytest
from fastapi.testclient import TestClient

from app.main import app, parse_json_object


VALID = {
    "company": "Acme",
    "fit_score": 87,
    "summary": "Strong API fit.",
    "risks": [],
    "next_action": "Book a call.",
}


def wrap(raw, form):
    if form == "fenced":
        return "```json\n" + raw + "\n```"
    if form == "embedded":
        return "Analysis follows:\n" + raw + "\nEnd."
    return raw


@pytest.mark.parametrize("form", ["direct", "fenced", "embedded"])
@pytest.mark.parametrize("raw", [
    '{"company":"First","company":"Second"}',
    '{"nested":{"key":1,"key":2}}',
    '{"nested":[{"key":1,"key":2}]}',
    '{"company":"First","comp\\u0061ny":"Second"}',
    '{"value":NaN}',
    '{"value":Infinity}',
    '{"value":-Infinity}',
    '{"nested":[{"value":NaN}]}',
    '{"value":1e999}',
    '{"value":-1e999}',
    '{"nested":[[{"value":1e999}]]}',
    '{"nested":[[{"value":-1e999}]]}',
])
def test_parser_rejects_invalid_members_and_numbers(raw, form):
    with pytest.raises(ValueError):
        parse_json_object(wrap(raw, form))


@pytest.mark.parametrize("form", ["direct", "fenced", "embedded"])
@pytest.mark.parametrize("member", [
    '"company":"First",',
    '"extra":{"key":1,"key":2},',
    '"extra":NaN,',
    '"extra":Infinity,',
    '"extra":-Infinity,',
    '"extra":1e999,',
    '"extra":-1e999,',
    '"extra":[[{"value":1e999}]],',
    '"extra":[[{"value":-1e999}]],',
])
def test_endpoint_reports_invalid_json(member, form):
    raw = "{" + member + json.dumps(VALID)[1:]
    response = TestClient(app).post("/validate", json={"raw": wrap(raw, form)})
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert body["data"] is None
    assert body["error"]["code"] == "INVALID_JSON"
    assert body["error"]["details"] == []


@pytest.mark.parametrize("form", ["direct", "fenced", "embedded"])
def test_valid_text_and_nested_objects_are_preserved(form):
    expected = {"nested": [{"key": 1}, {"key": 2}], "text": "NaN Infinity {braces}"}
    assert parse_json_object(wrap(json.dumps(expected), form)) == expected
