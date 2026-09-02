"""Observable task-progress reporting for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from threading import RLock
from typing import Callable


@dataclass(frozen=True)
class ProgressEvent:
    task_id: str
    status: str
    progress: float
    message: str
    timestamp: datetime


class ProgressReporter:
    """Publishes bounded progress events to local subscribers."""

    def __init__(self) -> None:
        self._events: list[ProgressEvent] = []
        self._listeners: list[Callable[[ProgressEvent], None]] = []
        self._lock = RLock()

    def report(self, task_id: str, status: str, progress: float, message: str = "") -> ProgressEvent:
        if not task_id.strip():
            raise ValueError("task_id is required")
        if not 0.0 <= progress <= 1.0:
            raise ValueError("progress must be between 0 and 1")
        event = ProgressEvent(
            task_id.strip(), status.strip().lower(), progress, message,
            datetime.now(timezone.utc),
        )
        with self._lock:
            self._events.append(event)
            listeners = tuple(self._listeners)
        for listener in listeners:
            listener(event)
        return event

    def subscribe(self, listener: Callable[[ProgressEvent], None]) -> None:
        with self._lock:
            if listener not in self._listeners:
                self._listeners.append(listener)

    def recent(self, limit: int = 20) -> tuple[ProgressEvent, ...]:
        if limit < 1:
            return ()
        with self._lock:
            return tuple(self._events[-limit:])
