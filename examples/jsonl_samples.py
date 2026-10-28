"""Provide sanitized example model outputs for offline acceptance checks."""
import json


def samples():
    good = {"company": "Demo Labs", "fit_score": 80, "summary": "Test input", "risks": [], "next_action": "Follow up"}
    valid = json.dumps(good, separators=(",", ":"))
    return [valid, valid.replace('"fit_score":80', '"fit_score":"80"'), valid + " " + valid, '{"broken":']
