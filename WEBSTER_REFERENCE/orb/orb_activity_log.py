"""Compact local activity logging for Floating Orb interactions."""
from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from time import time


@dataclass(frozen=True)
class OrbActivity:
    event: str
    message: str
    timestamp: float


class OrbActivityLog:
    """Bounded log that stores interaction metadata, not screenshots or audio."""

    def __init__(self, *, max_entries: int = 200) -> None:
        if max_entries < 1:
            raise ValueError("max_entries must be positive")
        self._max_entries = max_entries
        self._entries: list[OrbActivity] = []
        self._lock = RLock()

    def append(self, event: str, message: str = "") -> OrbActivity:
        item = OrbActivity(event.strip(), message, time())
        with self._lock:
            self._entries.append(item)
            if len(self._entries) > self._max_entries:
                del self._entries[:-self._max_entries]
        return item

    def snapshot(self) -> tuple[OrbActivity, ...]:
        with self._lock:
            return tuple(self._entries)

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
