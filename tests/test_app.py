import json

from fastapi.testclient import TestClient

from app.main import app, parse_json_object

client = TestClient(app)

VALID = {
    "company": "Acme Labs",
    "fit_score": 87,
    "summary": "Strong API fit.",
    "risks": ["Small engineering team"],
    "next_action": "Book a technical discovery call.",
}

def post_raw(raw: str):
    return client.post("/validate", json={"raw": raw})

def test_health():
    assert client.get("/health").json() == {"status": "ok"}

def test_plain_json_happy_path():
    body = post_raw(json.dumps(VALID)).json()
    assert body["ok"] is True
    assert body["data"]["fit_score"] == 87

def test_fenced_json():
    raw = "```json\n" + json.dumps(VALID) + "\n```"
    assert post_raw(raw).json()["ok"] is True

def test_leading_and_trailing_prose():
    raw = "Analysis follows:\n" + json.dumps(VALID) + "\nEnd."
    assert post_raw(raw).json()["ok"] is True

def test_irrecoverable_malformed_json_is_rejected():
    body = post_raw('{"company": "Acme", "fit_score": 70').json()
    assert body["ok"] is False
    assert body["error"]["code"] == "INVALID_JSON"

def test_out_of_range_score_is_rejected():
    bad = {**VALID, "fit_score": 101}
    body = post_raw(json.dumps(bad)).json()
    assert body["ok"] is False
    assert body["error"]["code"] == "SCHEMA_VALIDATION_FAILED"

def test_wrong_type_is_rejected_not_coerced():
    bad = {**VALID, "fit_score": "87"}
    body = post_raw(json.dumps(bad)).json()
    assert body["ok"] is False

def test_missing_required_field_is_rejected():
    bad = dict(VALID)
    bad.pop("next_action")
    body = post_raw(json.dumps(bad)).json()
    assert body["ok"] is False

def test_top_level_array_is_rejected():
    body = post_raw('[{"company":"Acme"}]').json()
    assert body["ok"] is False
    assert body["error"]["code"] == "INVALID_JSON"

def test_no_fabricated_repair_of_broken_json():
    raw = 'prefix {"company": "Acme", "fit_score": 80, BROKEN} suffix'
    body = post_raw(raw).json()
    assert body["ok"] is False
    assert body["error"]["code"] == "INVALID_JSON"

def test_balanced_braces_inside_strings_do_not_break_extraction():
    good = {**VALID, "summary": "Handles braces like {example} safely."}
    raw = "Model output: " + json.dumps(good)
    assert parse_json_object(raw)["summary"].startswith("Handles braces")

def test_multiple_valid_json_objects_are_rejected_as_ambiguous():
    first = json.dumps(VALID)
    second = json.dumps({**VALID, "company": "Other Co"})
    body = post_raw(first + "\n" + second).json()
    assert body["ok"] is False
    assert body["error"]["code"] == "AMBIGUOUS_JSON"
