"""Tests for the command execution safety boundary."""
from __future__ import annotations

from WEBSTER_REFERENCE.core.command_contracts import CommandRequest
from WEBSTER_REFERENCE.core.execution import ExecutionBoundary


def test_unexpected_handler_exception_becomes_response() -> None:
    request = CommandRequest("test")

    def broken(_request: CommandRequest) -> str:
        raise RuntimeError("secret implementation detail")

    result = ExecutionBoundary().execute(request, broken)
    assert not result.response.ok
    assert result.response.error_code == "COMMAND_EXECUTION_ERROR"
    assert "secret implementation detail" not in result.response.message
