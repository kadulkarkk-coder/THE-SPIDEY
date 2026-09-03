"""Lightweight validation for tool call arguments."""
from __future__ import annotations
from .tool_contract import ToolBinding, ToolCall
from .tool_errors import ToolValidationError

class ToolValidator:
    def validate(self, binding: ToolBinding, call: ToolCall) -> None:
        expected = set(binding.spec.parameters)
        supplied = set(call.arguments)
        missing = expected - supplied
        if missing:
            raise ToolValidationError(f"missing arguments: {', '.join(sorted(missing))}")
        if not supplied.issubset(expected):
            extra = supplied - expected
            raise ToolValidationError(f"unexpected arguments: {', '.join(sorted(extra))}")
