"""WEBSTER application runtime with the Sprint 3 command pipeline."""
from __future__ import annotations

from datetime import datetime, timezone
from time import monotonic
from typing import Any
from uuid import uuid4

from .command_contracts import CommandRequest, CommandResponse
from .command_dispatcher import CommandDispatcher
from .component_registry import ComponentRegistry
from .config import WebsterConfig
from .diagnostics import Diagnostics
from .errors import CommandError
from .event_bus import EventBus
from .health_monitor import HealthMonitor
from .lifecycle import LifecycleManager, LifecycleState
from .runtime_context import RuntimeContext
from .service_registry import ServiceRegistry


class WebsterApplication:
    """Dependency-free WEBSTER runtime foundation."""

    VERSION = "0.1.0-alpha"

    def __init__(self, config: WebsterConfig | None = None) -> None:
        self.config = config or WebsterConfig.from_environment()
        self.events = EventBus()
        self.health = HealthMonitor()
        self.lifecycle = LifecycleManager()
        self.components = ComponentRegistry()
        self.services = ServiceRegistry()
        self.diagnostics = Diagnostics()
        self.context = RuntimeContext(session_id=uuid4().hex)
        self.commands = CommandDispatcher()
        self.started_at: datetime | None = None
        self._register_core_components()
        self._register_commands()

    def _register_core_components(self) -> None:
        self.health.register("event_bus")
        self.health.register("health_monitor")
        self.health.register("lifecycle")
        self.health.register("command_dispatcher")
        self.components.register("event_bus", self.events, "In-process event bus")
        self.components.register("health_monitor", self.health, "Runtime health state")
        self.components.register("lifecycle", self.lifecycle, "Application lifecycle")
        self.components.register("command_dispatcher", self.commands, "Command routing")
        self.services.register_service("diagnostics", self.diagnostics, "Runtime metrics")

    def _register_commands(self) -> None:
        self.commands.register("help", self._command_help)
        self.commands.register("status", self._command_status)
        self.commands.register("diagnostics", self._command_diagnostics)
        self.commands.register("context", self._command_context)
        self.commands.register("exit", self._command_exit)
        self.commands.register("quit", self._command_exit)

    def start(self) -> None:
        if self.lifecycle.state is LifecycleState.RUNNING:
            return
        try:
            self.lifecycle.start()
            self.started_at = datetime.now(timezone.utc)
            self.events.publish("system.started", {"version": self.VERSION})
        except Exception as exc:
            self.lifecycle.fail()
            self.health.set_status("lifecycle", "failed", healthy=False, detail=str(exc))
            raise

    def stop(self) -> None:
        if self.lifecycle.state is not LifecycleState.RUNNING:
            return
        self.events.publish("system.stopping")
        self.lifecycle.stop()
        self.events.publish("system.stopped")

    def status(self) -> dict[str, Any]:
        return {
            "name": self.config.name,
            "version": self.VERSION,
            "environment": self.config.environment,
            "running": self.lifecycle.state is LifecycleState.RUNNING,
            "state": self.lifecycle.state.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "components": self.health.component_count,
            "commands": self.commands.count(),
            "healthy": self.health.is_healthy(),
        }

    def handle(self, request: CommandRequest) -> CommandResponse:
        """Run one request through dispatch, error handling, events, and metrics."""
        started = monotonic()
        try:
            response = self.commands.dispatch(request)
        except CommandError as exc:
            response = CommandResponse.failure(request.normalized(), str(exc), exc.__class__.__name__.upper())
        except Exception as exc:
            response = CommandResponse.failure(request.normalized(), "Internal runtime error.", "INTERNAL_ERROR")
            self.events.publish("command.error", {"request_id": request.request_id, "error": str(exc)})
        self.diagnostics.record(ok=response.ok, started_at=started)
        self.events.publish("command.completed", {"request_id": request.request_id, "ok": response.ok})
        return response

    def command(self, text: str) -> str:
        """Backward-compatible text command API for the CLI."""
        return self.handle(CommandRequest(text)).message

    def _command_help(self, request: CommandRequest) -> str:
        return "Available commands: " + ", ".join(self.commands.names())

    def _command_status(self, request: CommandRequest) -> str:
        return str(self.status())

    def _command_diagnostics(self, request: CommandRequest) -> str:
        return str(self.diagnostics.as_dict())

    def _command_context(self, request: CommandRequest) -> str:
        return str(self.context.snapshot())

    def _command_exit(self, request: CommandRequest) -> str:
        self.stop()
        return "WEBSTER stopped."
