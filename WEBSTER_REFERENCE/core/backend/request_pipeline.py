"""Request processing pipeline connecting intent, dispatch and diagnostics."""
from __future__ import annotations

from time import monotonic

from .command_contracts import CommandRequest, CommandResponse
from .command_dispatcher import CommandDispatcher
from .diagnostics import Diagnostics
from .errors import WebsterError
from .execution import ExecutionBoundary
from .intent import parse_intent


class RequestPipeline:
    """Single deterministic entry point for runtime requests."""

    def __init__(self, dispatcher: CommandDispatcher, diagnostics: Diagnostics) -> None:
        self.dispatcher = dispatcher
        self.diagnostics = diagnostics
        self.execution = ExecutionBoundary()

    def process(self, request: CommandRequest) -> CommandResponse:
        started = monotonic()
        request = request.normalized()
        try:
            intent = parse_intent(request.text)
            if not intent.name:
                raise WebsterError("Command cannot be empty")
            handler = self.dispatcher.handler_for(intent.name)
            response = self.execution.execute(request, handler).response
            self.diagnostics.record(ok=response.ok, started_at=started)
            return response
        except WebsterError as exc:
            response = CommandResponse.failure(request, str(exc), exc.__class__.__name__.upper())
            self.diagnostics.record(ok=False, started_at=started)
            return response
