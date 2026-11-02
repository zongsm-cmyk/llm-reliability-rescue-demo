"""
LoopControl - Networked API Reliability & Circuit Breaker Harness
Module: loopcontrol_api_fallback.py
Target: hello@loopcontrol.io
"""

from __future__ import annotations
import time
import logging
from typing import Any, Callable, Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("LoopControl.CircuitBreaker")

class CircuitState:
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class NetworkCircuitBreaker:
    """Implements industrial circuit-breaker with automatic recovery."""
    
    def __init__(self, failure_threshold: int = 3, recovery_time: float = 1.0):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0

    def call(self, func: Callable[..., Any], *args: Any, fallback: Callable[..., Any] = None, **kwargs: Any) -> Any:
        now = time.time()
        if self.state == CircuitState.OPEN:
            if now - self.last_failure_time > self.recovery_time:
                logger.info("Circuit breaker entering HALF_OPEN state; testing upstream health...")
                self.state = CircuitState.HALF_OPEN
            else:
                logger.warning("Circuit breaker OPEN. Routing directly to offline fallback.")
                if fallback:
                    return fallback(*args, **kwargs)
                raise RuntimeError("Circuit breaker is OPEN and no fallback provided.")

        try:
            result = func(*args, **kwargs)
            if self.state == CircuitState.HALF_OPEN:
                logger.info("Probe succeeded. Circuit reset to CLOSED.")
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            return result
        except Exception as exc:
            self.failure_count += 1
            self.last_failure_time = now
            logger.error("Upstream invocation failed (%d/%d): %s", self.failure_count, self.failure_threshold, exc)
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                logger.error("Failure threshold reached! Circuit trip to OPEN.")
            if fallback:
                return fallback(*args, **kwargs)
            raise

def run_tests():
    print("=== RUNNING LOOPCONTROL API RELIABILITY HARNESS ===")
    breaker = NetworkCircuitBreaker(failure_threshold=2, recovery_time=0.5)

    def failing_api():
        raise ConnectionResetError("Remote host forcibly closed an existing connection")

    def fallback_handler():
        return {"status": "fallback_healthy", "cached_response": True}

    # Calls 1 & 2 fail, tripping breaker
    res1 = breaker.call(failing_api, fallback=fallback_handler)
    assert res1["status"] == "fallback_healthy"
    res2 = breaker.call(failing_api, fallback=fallback_handler)
    assert res2["status"] == "fallback_healthy"
    assert breaker.state == CircuitState.OPEN
    print("[PASS] Circuit successfully tripped to OPEN after 2 failures.")

    # Call 3 routed instantly to fallback without hitting network
    res3 = breaker.call(failing_api, fallback=fallback_handler)
    assert res3["cached_response"] is True
    print("[PASS] Fallback served while circuit is OPEN.")

    # Recovery test
    time.sleep(0.6)
    def recovered_api():
        return {"status": "live_200_ok"}

    res4 = breaker.call(recovered_api, fallback=fallback_handler)
    assert res4["status"] == "live_200_ok"
    assert breaker.state == CircuitState.CLOSED
    print("[PASS] Circuit safely reset to CLOSED upon recovery.")
    print("=== LOOPCONTROL VERIFICATION 100% COMPLETE ===")

if __name__ == "__main__":
    run_tests()
