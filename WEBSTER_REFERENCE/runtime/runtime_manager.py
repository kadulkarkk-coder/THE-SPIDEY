"""Own the real WEBSTER runtime lifecycle without owning UI, camera or microphone loops."""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .resource_guard import ResourceGuard
from .runtime_state import RuntimeSnapshot, RuntimeState
from .startup_checks import StartupChecks


class RuntimeManager:
    """Start, monitor and stop WEBSTER services deterministically."""

    def __init__(self) -> None:
        self.state = RuntimeState.CREATED
        self.started_at: str | None = None
        self.stopped_at: str | None = None
        self.request_count = 0
        self.error_count = 0
        self.last_error: str | None = None
        self._services: list[tuple[str, Callable[[], None], Callable[[], None]]] = []
        self.checks = StartupChecks()
        self.resources = ResourceGuard()

    def register_service(
        self,
        name: str,
        start: Callable[[], None],
        stop: Callable[[], None],
    ) -> None:
        if any(existing == name for existing, _, _ in self._services):
            raise ValueError(f"Runtime service already registered: {name}")
        self._services.append((name, start, stop))

    def start(self) -> None:
        if self.state is RuntimeState.RUNNING:
            return
        self.state = RuntimeState.STARTING
        report = self.checks.summary()
        if not report["ok"]:
            self.state = RuntimeState.FAILED
            failed = [item["name"] for item in report["checks"] if not item["ok"]]
            raise RuntimeError(f"Startup checks failed: {', '.join(failed)}")
        started: list[tuple[str, Callable[[], None], Callable[[], None]]] = []
        try:
            for service in self._services:
                name, start, stop = service
                start()
                started.append(service)
            self.started_at = RuntimeSnapshot.now()
            self.stopped_at = None
            self.state = RuntimeState.RUNNING
        except Exception as exc:
            self.last_error = str(exc)
            self.error_count += 1
            for _, _, stop in reversed(started):
                try:
                    stop()
                except Exception:
                    pass
            self.state = RuntimeState.FAILED
            raise

    def stop(self) -> None:
        if self.state in {RuntimeState.STOPPED, RuntimeState.CREATED}:
            self.state = RuntimeState.STOPPED
            return
        self.state = RuntimeState.STOPPING
        for _, _, stop in reversed(self._services):
            try:
                stop()
            except Exception as exc:
                self.last_error = str(exc)
                self.error_count += 1
        self.stopped_at = RuntimeSnapshot.now()
        self.state = RuntimeState.STOPPED

    def record_request(self, ok: bool) -> None:
        self.request_count += 1
        if not ok:
            self.error_count += 1

    def snapshot(self) -> dict[str, Any]:
        runtime = RuntimeSnapshot(
            state=self.state,
            started_at=self.started_at,
            stopped_at=self.stopped_at,
            request_count=self.request_count,
            error_count=self.error_count,
            last_error=self.last_error,
            metadata={"resource_budget_ok": self.resources.budget_ok()},
        )
        return runtime.as_dict()
