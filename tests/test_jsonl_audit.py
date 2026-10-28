import io
import json
from examples.jsonl_audit import check, run

GOOD = {"company": "Acme", "fit_score": 80, "summary": "Yes", "next_action": "Email"}


def test_valid_and_no_raw_data():
    result = check(json.dumps(GOOD), 1)
    assert result == {"line": 1, "ok": True, "fit_score": 80}
    assert "Acme" not in str(result)


def test_rejects_malformed_and_ambiguous():
    assert check('{"company":', 1)["code"] == "INVALID_JSON"
    assert check(json.dumps(GOOD) * 2, 2)["code"] == "AMBIGUOUS_JSON"


def test_schema_and_raw_input_rejected():
    assert check(json.dumps({**GOOD, "fit_score": "80"}), 1)["code"] == "SCHEMA_VALIDATION_FAILED"
    assert check("\n", 2)["code"] == "INVALID_INPUT"


def test_batch_line_numbers_and_counts():
    dst = io.StringIO()
    assert run(io.StringIO(json.dumps(GOOD) + "\n" + "{broken\n"), dst) == (2, 1)
    assert [json.loads(s)["line"] for s in dst.getvalue().splitlines()] == [1, 2]
