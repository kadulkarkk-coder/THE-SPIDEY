"""WEBSTER core health monitoring.

Sprint 1 implementation: tracks component registration, state, and health.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from threading import RLock


@dataclass(slots=True)
class ComponentHealth:
    name: str
    healthy: bool = True
    status: str = "ready"
    detail: str = ""
    checked_at: datetime | None = None

    def check(self) -> None:
        self.checked_at = datetime.now(timezone.utc)


class HealthMonitor:
    """Thread-safe registry of WEBSTER component health."""

    def __init__(self) -> None:
        self._components: dict[str, ComponentHealth] = {}
        self._lock = RLock()

    def register(self, name: str, *, status: str = "ready", detail: str = "") -> None:
        if not name.strip():
            raise ValueError("component name must not be empty")
        with self._lock:
            component = ComponentHealth(name=name, status=status, detail=detail)
            component.check()
            self._components[name] = component

    def set_status(self, name: str, status: str, *, healthy: bool = True, detail: str = "") -> None:
        with self._lock:
            if name not in self._components:
                self.register(name)
            component = self._components[name]
            component.status = status
            component.healthy = healthy
            component.detail = detail
            component.check()

    def is_healthy(self) -> bool:
        with self._lock:
            return all(component.healthy for component in self._components.values())

    def snapshot(self) -> dict[str, dict[str, object]]:
        with self._lock:
            return {
                name: {
                    "healthy": item.healthy,
                    "status": item.status,
                    "detail": item.detail,
                    "checked_at": item.checked_at.isoformat() if item.checked_at else None,
                }
                for name, item in self._components.items()
            }

    @property
    def component_count(self) -> int:
        with self._lock:
            return len(self._components)
