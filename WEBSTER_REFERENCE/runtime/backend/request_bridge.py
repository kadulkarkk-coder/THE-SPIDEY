"""Functional request bridge between clients and the WEBSTER core pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Any

from ..core.command_contracts import CommandRequest, CommandResponse
from ..core.request_pipeline import RequestPipeline
from .runtime_manager import RuntimeManager


@dataclass(frozen=True)
class RuntimeRequestEvent:
    """Small immutable event emitted after a request reaches the core."""

    request_id: str
    ok: bool
    error_code: str | None
    duration_ms: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "ok": self.ok,
            "error_code": self.error_code,
            "duration_ms": round(self.duration_ms, 3),
        }


class RuntimeRequestBridge:
    """Single dependable entry point for desktop, voice, remote and tests."""

    def __init__(self, pipeline: RequestPipeline, runtime: RuntimeManager, event_publisher: Any = None) -> None:
        self.pipeline = pipeline
        self.runtime = runtime
        self.event_publisher = event_publisher

    def submit(self, request: CommandRequest) -> CommandResponse:
        """Process exactly one request and convert unexpected failures to a response."""
        started = monotonic()
        if self.runtime.state.value not in {"running", "degraded"}:
            response = CommandResponse.failure(request, "WEBSTER runtime is not running.", "RUNTIME_NOT_RUNNING")
        else:
            try:
                response = self.pipeline.process(request)
            except Exception as exc:  # final runtime safety boundary
                response = CommandResponse.failure(
                    request,
                    "The request could not be completed safely.",
                    "INTERNAL_RUNTIME_ERROR",
                )
        duration_ms = (monotonic() - started) * 1000.0
        self.runtime.record_request(response.ok)
        event = RuntimeRequestEvent(request.request_id, response.ok, response.error_code, duration_ms)
        if self.event_publisher is not None:
            self.event_publisher.publish(
                "runtime.request.completed" if response.ok else "runtime.request.failed",
                event.as_dict(),
            )
        return response
