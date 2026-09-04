"""Thread-safe Floating Orb state store."""
from __future__ import annotations

from threading import RLock

from .orb_types import OrbEvent, OrbState


class OrbStateStore:
    """Keep presentation state separate from the eventual UI toolkit."""

    def __init__(self) -> None:
        self._event = OrbEvent(OrbState.HIDDEN)
        self._lock = RLock()

    def set(self, state: OrbState, message: str = "") -> OrbEvent:
        event = OrbEvent(state, message)
        with self._lock:
            self._event = event
        return event

    def snapshot(self) -> OrbEvent:
        with self._lock:
            return self._event
