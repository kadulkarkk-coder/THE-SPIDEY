"""A6 action-routing tests."""
from __future__ import annotations
from WEBSTER_REFERENCE.intelligence.action_router import ActionRouter
from WEBSTER_REFERENCE.intelligence.intent_pipeline import IntelligencePipeline
from WEBSTER_REFERENCE.tools.tool_contract import ToolBinding, ToolSpec
from WEBSTER_REFERENCE.tools.tool_dispatcher import ToolDispatcher
from WEBSTER_REFERENCE.tools.tool_registry import ToolRegistry

def _tools() -> ToolDispatcher:
    from WEBSTER_REFERENCE.intelligence.local_calculator import calculate
    from datetime import datetime
    registry = ToolRegistry()
    registry.register(ToolBinding(ToolSpec("calculator", "safe arithmetic", frozenset({"local.compute"})), calculate))
    registry.register(ToolBinding(ToolSpec("time", "local time", frozenset({"runtime.read"})), lambda: datetime.now().astimezone().strftime("%H:%M")))
    return ToolDispatcher(registry)

def test_calculate_routes_and_executes() -> None:
    interpretation = IntelligencePipeline().interpret("calculate 12 * 7")
    result = ActionRouter(tool_dispatcher=_tools()).route(interpretation, request_id="a6")
    assert result.handled and result.ok and result.target == "calculator" and result.message == "84"

def test_time_routes_and_executes() -> None:
    interpretation = IntelligencePipeline().interpret("what time is it")
    result = ActionRouter(tool_dispatcher=_tools()).route(interpretation, request_id="a6")
    assert result.handled and result.ok and result.target == "time"

def test_command_target_routes_without_recursion() -> None:
    interpretation = IntelligencePipeline().interpret("help me")
    calls = []
    result = ActionRouter(command_handler=lambda name: calls.append(name) or "help", tool_dispatcher=_tools()).route(interpretation)
    assert result.handled and result.ok and calls == ["help"]
