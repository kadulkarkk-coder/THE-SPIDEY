"""Runtime state shared by functional WEBSTER frontends."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class RuntimeState(str, Enum):
    CREATED = "created"
    STARTING = "starting"
    RUNNING = "running"
    DEGRADED = "degraded"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass
class RuntimeSnapshot:
    state: RuntimeState
    started_at: str | None
    stopped_at: str | None
    request_count: int = 0
    error_count: int = 0
    last_error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "state": self.state.value,
            "started_at": self.started_at,
            "stopped_at": self.stopped_at,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "last_error": self.last_error,
            "metadata": dict(self.metadata),
        }

    @staticmethod
    def now() -> str:
        return datetime.now(timezone.utc).isoformat()
