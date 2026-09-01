"""WEBSTER application runtime.

Sprint 1 implementation: wires the first core services into a runnable application.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .event_bus import EventBus
from .health_monitor import HealthMonitor
from .lifecycle import LifecycleManager, LifecycleState


class WebsterApplication:
    """Dependency-free WEBSTER runtime foundation."""

    VERSION = "0.1.0-alpha"

    def __init__(self) -> None:
        self.events = EventBus()
        self.health = HealthMonitor()
        self.lifecycle = LifecycleManager()
        self.started_at: datetime | None = None
        self._register_core_components()

    def _register_core_components(self) -> None:
        self.health.register("event_bus")
        self.health.register("health_monitor")
        self.health.register("lifecycle")

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
            "name": "WEBSTER",
            "version": self.VERSION,
            "running": self.lifecycle.state is LifecycleState.RUNNING,
            "state": self.lifecycle.state.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "components": self.health.component_count,
            "healthy": self.health.is_healthy(),
        }

    def command(self, text: str) -> str:
        """Handle the tiny Sprint-1 command surface."""
        command = text.strip().lower()
        if command == "help":
            return "Available commands: help, status, exit"
        if command == "status":
            return str(self.status())
        if command in {"exit", "quit"}:
            self.stop()
            return "WEBSTER stopped."
        return f"Unknown command: {command}. Type 'help'."
