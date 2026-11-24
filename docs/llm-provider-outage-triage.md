# LLM provider outage triage — free 10-minute runbook

A practical, vendor-neutral checklist for Python and API engineers handling **429s, timeouts, malformed model JSON and failing fallback paths**. This is an educational guide from Askoure Tools; it is free to use and does not require a paid kit.

## 1. Identify the failure boundary before changing retry logic

| Symptom | First thing to verify | Common incorrect response |
| --- | --- | --- |
| HTTP 429 / quota response | Status, provider request ID, retry-after header, quota scope | Unlimited immediate retries |
| Timeout / connection reset | Caller deadline, request duration, partial downstream side effects | Blind replay of a non-idempotent request |
| HTTP 5xx | Upstream error class, regional status page, rolling error rate | Treating every error as permanent |
| JSON parse or schema error | Sanitized raw content sample, contract/schema version | Silently fabricating fields to make parsing pass |
| Fallback appears successful but data is missing | Selected provider, model/version, output contract, persisted result ID | Counting a substitute response as equivalent without validation |

**First action:** capture a redacted request ID, UTC timestamp, provider/model identifier, status class, deadline, retry count and output validation result. Do not log raw secrets, customer prompts or personal data.

## 2. Establish your call budget

Write down the end-to-end deadline of the user request and reserve time for validation and application cleanup. If the remaining budget cannot support a full fallback call, return an explicit failure instead of triggering another request that cannot finish.

A bounded policy to discuss with your team:

- Only retry when the failure is **known to be retryable** under the provider's rules.
- Honor `Retry-After` when present; use bounded jittered backoff when appropriate.
- Cap attempts **and** total elapsed time. Distinguish provider errors from client-side schema failures.
- Retry write operations only when idempotency and side-effect semantics are understood.
- Stop retry storms at the caller and, when available, with a circuit breaker.

## 3. Verify circuit-breaker behavior with four tests

1. **Closed → Open:** repeated qualifying failures within the configured sampling window cause subsequent calls to fail fast.
2. **Open → Half-open:** after the cooldown, allow a tightly controlled probe; avoid a thundering herd.
3. **Half-open → Closed:** a successful probe meeting the actual response contract permits normal traffic again.
4. **Half-open → Open:** a failing probe reopens the breaker; record the reason and next eligible probe time.

A breaker is not a replacement for request deadlines, an actual fallback provider, or durable handling of unfinished jobs.

## 4. Test the fallback contract, not just the HTTP status

When switching providers or models, check **response schema, version-specific formatting, token limits, model capability, output safety and business semantics**. Successful HTTP status alone is not an acceptable downstream result.

Use a redacted, synthetic failing case and assert that the fallback returns the expected fields without fabricated default values. If the contract fails, surface an explicit error.

## 5. Track unsuccessful jobs without claiming zero data loss

For asynchronous processing, consider an explicit dead-letter record containing a safe job reference, failure class, attempt count and reprocessing state. A local SQLite example can demonstrate the pattern; production durability, concurrent access, backups and recovery require separate architecture decisions and testing.

**Do not** claim “zero lost requests,” guaranteed uptime or production savings without measured evidence and a suitable durability design.

## 6. Five pieces of evidence to collect for a credible before/after comparison

- One reproducible sanitized failure case.
- Current and target policy with exact timeout, attempt and fallback limits.
- Counts of accepted, rejected, retried and dead-lettered requests for comparable test runs.
- Latency distribution and upstream error-rate measurements from the same conditions.
- A regression suite covering success, 429, timeout, malformed JSON and failed fallback.

The **free open-source demo** provides [strict JSON validation tests](../tests/) and [resilience examples](../solutions/resilience-shields/). It does not establish results from an external client's production workload.

---

## Optional ready-to-use toolkit

If you need packaged examples rather than adapting the free references, the separate commercial **[LLM Reliability Rescue Kit — $7 with EARLY30DEV (regular $10)](https://mhamedasskoure.gumroad.com/l/lujvp/EARLY30DEV?utm_source=github&utm_medium=free_triage_runbook&utm_campaign=llm_failure_diagnostic_20261124)** includes Python circuit-breaker and provider-fallback examples, SQLite dead-letter queue resources, tests and documentation. Review the listing, environment requirements and license before purchasing. The price shown is the eligible promotional price before any applicable taxes; no deadline or scarcity claim is implied.

For an estimate-and-reliability bundle, [Agency Tech Master Bundle — $15.33 with EARLY30DEV (regular $21.90)](https://mhamedasskoure.gumroad.com/l/ktkuv/EARLY30DEV?utm_source=github&utm_medium=free_triage_runbook&utm_campaign=llm_failure_diagnostic_20261124) also includes the separate CleanQuote Estimation System. **Neither product promises production deployment or guaranteed savings.**

Need help with one reproducible Python/API bug instead? See the [$95 fixed-scope engineering service](https://mhamedasskoure.gumroad.com/l/python-api-scoped-commission?utm_source=github&utm_medium=free_triage_runbook&utm_campaign=llm_failure_diagnostic_20261124), with scope and acceptance agreed before purchase.

*Disclosure: Askoure Tools sells these paid products. This entire runbook remains free and usable without a purchase.*
