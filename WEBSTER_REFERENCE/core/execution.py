"""Safe execution boundary for WEBSTER command handlers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .command_contracts import CommandRequest, CommandResponse
from .errors import WebsterError


@dataclass(frozen=True)
class ExecutionResult:
    response: CommandResponse
    handled: bool = True


class ExecutionBoundary:
    """Executes approved callables and converts expected failures to responses."""

    def execute(
        self,
        request: CommandRequest,
        handler: Callable[[CommandRequest], str | CommandResponse],
    ) -> ExecutionResult:
        try:
            result = handler(request)
            if isinstance(result, CommandResponse):
                return ExecutionResult(result)
            return ExecutionResult(CommandResponse.success(request, str(result)))
        except WebsterError as exc:
            return ExecutionResult(
                CommandResponse.failure(request, str(exc), exc.__class__.__name__.upper())
            )
