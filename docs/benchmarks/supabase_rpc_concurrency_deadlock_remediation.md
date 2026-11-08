# PostgreSQL / Supabase RPC Deadlock and Serialization Retry Runbook

**Document type:** Engineering test guide for SQLSTATE 40P01 and 40001.  
**Evidence status:** No measured customer error-rate, CPU or connection recovery statistics are available in this repository.

## Failure modes to separate

- **40P01:** deadlock detected; the database aborts one participant to resolve a lock cycle.
- **40001:** serialization failure; the transaction cannot be committed under the requested isolation constraints.
- Transient connection or HTTP errors are different failure categories and should not automatically trigger an identical retry.

Blind retries can amplify load; never retry non-idempotent external side effects without a controlled design.

## Investigation procedure

1. Capture the exact SQLSTATE, transaction sequence, lock order and sanitized error logs.
2. Reproduce in staging with the same transaction isolation level, rows and concurrency.
3. Shorten transactions and make the lock acquisition order consistent across competing operations where possible.
4. Retry the **whole transaction**, not the final SQL statement alone, after an actual rollback. Use a small bounded attempt count and jitter.
5. Record attempt numbers, committed/aborted transactions and application-visible outcomes, without logging payload secrets.

Illustrative Python-style decision sequence (not a drop-in driver patch):

    for attempt in range(MAX_ATTEMPTS):
        try:
            with new_transaction() as tx:
                apply_business_operation(tx)
            break
        except DatabaseError as error:
            if error.sqlstate not in {"40P01", "40001"}:
                raise
            if attempt + 1 == MAX_ATTEMPTS:
                raise
            sleep_with_bounded_jitter(attempt)

**Important:** The example requires an actual database driver, transaction API and idempotency guarantees; none are supplied by this pseudocode.

## Acceptance evidence

Report aborts, successful commits, latency percentiles, duplicate side effects and lock-wait statistics for representative load **before and after** the change. Observe pool exhaustion separately; reducing deadlocks does not by itself fix a misconfigured pool.

A [standalone synthetic transient-error simulator](../../solutions/resilience-shields/celery_postgres_failover.py) exists in the repo. Its PASS output shows mock branch execution, **not** successful deployment against Supabase/PostgREST production.

No claim is made of 100% error elimination, specific CPU recovery or zero dropped connections.


---

## Evidence and purchasing boundaries

This document is an engineering method and sample, **not measured customer production results**. No customer data, deployment logs, before/after latency records, or independently verified ROI metrics are supplied here. Validate changes on your own staging workload and capture the measured before/after evidence before claiming a gain.

For a separate **single, reproducible Python/API code bug**, the published [Gumroad fixed-scope Commission ($95)](https://mhamedasskoure.gumroad.com/l/python-api-scoped-commission) is available after a free written scope check. It is **not** a general infrastructure deployment or an always-on operations service. No payment claim, no guarantee of zero downtime.