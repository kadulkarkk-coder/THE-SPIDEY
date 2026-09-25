"""Bounded security event audit trail for WEBSTER remote access."""
from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from time import time


@dataclass(frozen=True)
class SecurityEvent:
    event: str
    device_id: str
    allowed: bool
    detail: str
    timestamp: float


class SecurityEventLog:
    """Keep compact audit metadata without storing credentials or message contents."""

    def __init__(self, *, max_events: int = 200) -> None:
        if max_events < 1:
            raise ValueError("max_events must be positive")
        self._max_events = max_events
        self._events: list[SecurityEvent] = []
        self._lock = RLock()

    def record(self, event: str, device_id: str, allowed: bool, detail: str = "") -> SecurityEvent:
        item = SecurityEvent(event.strip(), device_id.strip(), allowed, detail, time())
        with self._lock:
            self._events.append(item)
            if len(self._events) > self._max_events:
                del self._events[:-self._max_events]
        return item

    def snapshot(self) -> tuple[SecurityEvent, ...]:
        with self._lock:
            return tuple(self._events)

    def clear(self) -> None:
        with self._lock:
            self._events.clear()
