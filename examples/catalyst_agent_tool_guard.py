"""
Catalyst Wayfare AI - Agent Tool Call Exception Shield & Schema Harness
Module: catalyst_agent_tool_guard.py
Target: hn@cwai.co
"""

from __future__ import annotations
import logging
from typing import Any, Callable, Dict, Optional
from pydantic import BaseModel, Field, ValidationError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Catalyst.ToolGuard")

class ToolExecutionResult(BaseModel):
    success: bool
    output: Optional[Any] = None
    error_type: Optional[str] = None
    fallback_applied: bool = False

class AgentToolParameterGuard:
    """Safeguards agent execution loops against bad JSON arguments and tool crashes."""
    
    @staticmethod
    def execute_guarded(tool_name: str, param_schema: type[BaseModel], raw_args: Dict[str, Any], tool_fn: Callable[..., Any]) -> ToolExecutionResult:
        # Step 1: Validate parameters strictly
        try:
            validated_args = param_schema.model_validate(raw_args)
        except ValidationError as val_err:
            logger.warning("Tool '%s' received invalid arguments: %s", tool_name, val_err.errors())
            return ToolExecutionResult(
                success=False,
                error_type="PARAMETER_VALIDATION_ERROR",
                output=f"Tool argument schema error: {val_err.errors()[0].get('msg')}"
            )

        # Step 2: Execute tool with exception shield
        try:
            res = tool_fn(**validated_args.model_dump())
            return ToolExecutionResult(success=True, output=res)
        except Exception as exec_err:
            logger.error("Tool '%s' crashed with runtime error: %s", tool_name, exec_err)
            return ToolExecutionResult(
                success=False,
                error_type="TOOL_EXECUTION_FAILURE",
                output=f"Tool failed cleanly: {str(exec_err)}",
                fallback_applied=True
            )

class SearchToolArgs(BaseModel):
    query: str = Field(min_length=2, max_length=500)
    top_k: int = Field(default=5, ge=1, le=50)

def run_tests():
    print("=== RUNNING CATALYST WAYFARE AI TOOL SHIELD HARNESS ===")
    guard = AgentToolParameterGuard()

    def live_search_tool(query: str, top_k: int):
        if "crash" in query:
            raise ConnectionError("Search cluster socket closed prematurely")
        return [f"Result #{i} for {query}" for i in range(1, top_k + 1)]

    # Test 1: Valid execution
    res1 = guard.execute_guarded("web_search", SearchToolArgs, {"query": "AI Agents", "top_k": 3}, live_search_tool)
    assert res1.success is True
    assert len(res1.output) == 3
    print("[PASS] Valid tool call verified.")

    # Test 2: Invalid parameter caught before execution
    res2 = guard.execute_guarded("web_search", SearchToolArgs, {"query": "", "top_k": 100}, live_search_tool)
    assert res2.success is False
    assert res2.error_type == "PARAMETER_VALIDATION_ERROR"
    print("[PASS] Malformed agent arguments caught cleanly without crashing the agent loop.")

    # Test 3: Tool runtime crash caught and shielded
    res3 = guard.execute_guarded("web_search", SearchToolArgs, {"query": "crash query", "top_k": 2}, live_search_tool)
    assert res3.success is False
    assert res3.fallback_applied is True
    assert res3.error_type == "TOOL_EXECUTION_FAILURE"
    print("[PASS] Tool runtime exception shielded from terminating agent session.")
    print("=== CATALYST WAYFARE VERIFICATION 100% COMPLETE ===")

if __name__ == "__main__":
    run_tests()
