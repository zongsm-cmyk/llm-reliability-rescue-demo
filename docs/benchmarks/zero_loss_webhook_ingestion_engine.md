# FastAPI Webhook Ingestion: Durable-ACK and Idempotency Design Checklist

**Document type:** Engineering blueprint, not an independently verified zero-loss system.  
**Evidence status:** No production traffic, measured acknowledgment latency or end-to-end loss audit is supplied here.

## Reliability boundary

An HTTP 2xx response is not proof of downstream processing success. A request can arrive twice, a sender can retry after a timeout, and a worker can crash after making a side effect but before recording completion. This design therefore aims at a **durable at-least-once intake**, not a guarantee of exactly-once effects or zero loss.

## Minimal safe flow

1. Authenticate the source: verify the provider-specific signature over the **raw request body**, using its documented timestamp tolerance and constant-time comparison.
2. Validate body size and event type; avoid putting payloads or secrets in error logs.
3. Extract a stable provider event ID and attempt an **atomic insert** into durable storage with a unique constraint on (provider, event_id).
4. Return a successful acknowledgement only after the transaction confirms durable acceptance. If persistence fails, return an appropriate retryable status according to the provider's contract.
5. Process accepted events in a worker with idempotent side effects and explicit retry/dead-letter handling.
6. Audit state transitions: received, queued, processing, succeeded, failed, retried, duplicate.
7. Handle a crash between side effect and completion acknowledgement; use an idempotency key, transactional outbox or downstream compensation where appropriate.

## Acceptance test matrix

| Failure | Required test |
| --- | --- |
| Forged or expired signature | reject without creating an event |
| Duplicate event ID | do not perform the side effect twice |
| Database unavailable | do not acknowledge durable acceptance |
| Worker dies after dequeue | recover event from durable queue |
| Sender retries after lost response | dedupe by stable event ID |
| Downstream timeout | bounded retry, idempotent side effect |
| Large payload | enforce body size limit |
| Slow queue at peak | measure acknowledgement latency and backlog |

Record *actual* p50/p95/p99 ACK latency, loss/retry observations, queue length and duplicate side effects. A <40ms acknowledgement or zero-loss claim cannot be made without those measurements.

## Existing related assets

- [n8n Workflow Preflight Auditor ($9)](https://mhamedasskoure.gumroad.com/l/n8n-workflow-preflight-auditor): offline **JSON structure** review, **not** live webhook delivery testing.
- [LLM Reliability Rescue Kit ($19)](https://mhamedasskoure.gumroad.com/l/llm-reliability-rescue-kit): model-output contracts, **not** a webhook gateway.
- [Python/API Commission ($95)](https://mhamedasskoure.gumroad.com/l/python-api-scoped-commission): one scoped coding deliverable, no deployment/hosting.


---

## Evidence and purchasing boundaries

This document is an engineering method and sample, **not measured customer production results**. No customer data, deployment logs, before/after latency records, or independently verified ROI metrics are supplied here. Validate changes on your own staging workload and capture the measured before/after evidence before claiming a gain.

For a separate **single, reproducible Python/API code bug**, the published [Gumroad fixed-scope Commission ($95)](https://mhamedasskoure.gumroad.com/l/python-api-scoped-commission) is available after a free written scope check. It is **not** a general infrastructure deployment or an always-on operations service. No payment claim, no guarantee of zero downtime.