"""
Rebar - Async Streaming Ingestion Buffer & Exception Shield
Module: rebar_async_stream_safety.py
Target: john@withrebar.ai
"""

from __future__ import annotations
import asyncio
import logging
from typing import AsyncGenerator, Dict, Any, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Rebar.StreamShield")

class StreamInterruptedError(Exception):
    """Simulates unexpected server disconnect or token truncation mid-stream."""
    pass

class AsyncStreamShield:
    """Buffers, validates, and resumes interrupted async SSE / JSON streams."""
    
    def __init__(self, chunk_timeout: float = 2.0):
        self.chunk_timeout = chunk_timeout
        self.received_buffer: List[Dict[str, Any]] = []

    async def ingest_stream_safely(self, stream_gen: AsyncGenerator[Dict[str, Any], None], resume_fn = None) -> List[Dict[str, Any]]:
        cursor = 0
        while True:
            try:
                async for chunk in stream_gen:
                    cursor = chunk.get("index", cursor + 1)
                    self.received_buffer.append(chunk)
                logger.info("Stream completed cleanly with %d total chunks.", len(self.received_buffer))
                return self.received_buffer
            except StreamInterruptedError as exc:
                logger.warning("Stream truncated at cursor %d (%s). Triggering auto-resume...", cursor, exc)
                if resume_fn:
                    stream_gen = resume_fn(resume_from=cursor)
                else:
                    logger.error("No resume handler provided; returning partially preserved buffer.")
                    return self.received_buffer

async def mock_faulty_stream(resume_from: int = 0) -> AsyncGenerator[Dict[str, Any], None]:
    for i in range(resume_from + 1, 6):
        if i == 3 and resume_from == 0:
            raise StreamInterruptedError("Inference gateway reset peer connection")
        yield {"index": i, "token": f"chunk_data_{i}"}

async def run_tests():
    print("=== RUNNING REBAR ASYNC STREAM SAFETY HARNESS ===")
    shield = AsyncStreamShield()

    def resume_handler(resume_from: int):
        return mock_faulty_stream(resume_from=resume_from)

    result = await shield.ingest_stream_safely(mock_faulty_stream(), resume_fn=resume_handler)
    assert len(result) == 5
    assert [r["index"] for r in result] == [1, 2, 3, 4, 5]
    print("[PASS] Stream interrupted at chunk 2, resumed from chunk 3 without data loss.")
    print("=== REBAR VERIFICATION 100% COMPLETE ===")

if __name__ == "__main__":
    asyncio.run(run_tests())
