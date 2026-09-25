"""Dispatch validated tool calls through registered handlers."""
from __future__ import annotations
from .tool_contract import ToolCall
from .tool_registry import ToolRegistry
from .tool_result import ToolResult

class ToolDispatcher:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def dispatch(self, call: ToolCall) -> ToolResult:
        binding = self.registry.get(call.name)
        if binding is None:
            return ToolResult.failure(call.name, "tool is not registered", code="NOT_FOUND", request_id=call.request_id)
        try:
            value = binding.handler(**call.arguments)
            return ToolResult.success(call.name, value, request_id=call.request_id)
        except Exception as exc:
            return ToolResult.failure(call.name, str(exc), code=exc.__class__.__name__.upper(), request_id=call.request_id)
