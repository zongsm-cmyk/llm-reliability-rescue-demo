# LLM Proxy Deadline Propagation and Retry Amplification — Test Runbook

**Document type:** Architecture review and deterministic test checklist.  
**Evidence status:** No real-proxy production reduction or 100% orphan-retry elimination has been measured here.

## Why ghost work happens

A user request times out at an ingress or client while a model proxy continues a retry delay or upstream attempt. The client may stop waiting even though work is still consuming provider resources. Cancellation is cooperative and may not undo a request already accepted by the provider.

## Bounded design

1. Set a **monotonic per-request deadline** at ingress and pass remaining budget to each downstream layer.
2. Before each retry, ensure retry delay **plus** a plausible call budget fits the remaining deadline.
3. Apply a low retry ceiling, jitter and an exponential schedule; honor Retry-After where appropriate without crossing the deadline.
4. Cancel tasks when possible. Do not assume cancellation prevented vendor-side inference or billing.
5. Use idempotency or a deduplicated request identifier for side effects; record retry decisions without exposing prompts, API keys or tokens.
6. Make terminal states visible: completed, cancelled, deadline exceeded, provider rejected or retry budget exhausted.

## Focused test cases

| Scenario | Expected decision |
| --- | --- |
| Deadline already exhausted | no new upstream dispatch |
| Retry-After beyond remaining deadline | stop instead of sleeping and retrying |
| Retryable provider error within budget | at most bounded attempt count |
| Cancellation during backoff | stop local scheduling; audit possible in-flight work |
| Rate limit plus multiple nested retry layers | avoid multiplying retry counts blindly |
| Missing idempotency for side-effectful call | require explicit risk decision |

Instrument attempts, cancellation outcomes and actual provider usage. Compare baseline versus patched proxy with matched synthetic traffic. Without that evidence, do not claim a percentage savings result.

## Related downloadable product

The [Agent Runaway Guard Kit ($24)](https://mhamedasskoure.gumroad.com/l/agent-runaway-guard-kit) provides separate **Python agent pre-dispatch controls** and synthetic replay checks. It does not automatically integrate with or modify a LiteLLM deployment. Confirm integration scope before purchase.

For a **single agreed code defect**, [Gumroad Python/API Commission ($95)](https://mhamedasskoure.gumroad.com/l/python-api-scoped-commission) offers written code deliverables; not emergency production support.


---

## Evidence and purchasing boundaries

This document is an engineering method and sample, **not measured customer production results**. No customer data, deployment logs, before/after latency records, or independently verified ROI metrics are supplied here. Validate changes on your own staging workload and capture the measured before/after evidence before claiming a gain.

For a separate **single, reproducible Python/API code bug**, the published [Gumroad fixed-scope Commission ($95)](https://mhamedasskoure.gumroad.com/l/python-api-scoped-commission) is available after a free written scope check. It is **not** a general infrastructure deployment or an always-on operations service. No payment claim, no guarantee of zero downtime.