"""Bounded observability for gesture events without retaining raw camera data."""
from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from time import monotonic


@dataclass(frozen=True)
class GestureObservation:
    operation: str
    gesture: str
    accepted: bool
    detail: str
    timestamp: float


class GestureObserver:
    """Keep only compact event metadata; never store frames or images."""

    def __init__(self, *, max_events: int = 100) -> None:
        if max_events < 1:
            raise ValueError("max_events must be positive")
        self._max_events = max_events
        self._events: list[GestureObservation] = []
        self._lock = Lock()

    def record(self, operation: str, gesture: str, accepted: bool, detail: str = "") -> None:
        event = GestureObservation(operation, gesture, accepted, detail, monotonic())
        with self._lock:
            self._events.append(event)
            if len(self._events) > self._max_events:
                del self._events[:-self._max_events]

    def snapshot(self) -> tuple[GestureObservation, ...]:
        with self._lock:
            return tuple(self._events)
