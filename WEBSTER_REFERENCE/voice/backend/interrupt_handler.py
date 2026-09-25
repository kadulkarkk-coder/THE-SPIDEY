"""Safe interruption and conversational turn control."""
from __future__ import annotations
from dataclasses import dataclass
from threading import RLock

@dataclass(frozen=True)
class InterruptState:
    interrupted: bool = False
    reason: str = ""

class InterruptHandler:
    def __init__(self) -> None:
        self._state = InterruptState()
        self._lock = RLock()

    def request(self, reason: str = "user") -> InterruptState:
        with self._lock:
            self._state = InterruptState(True, reason.strip() or "user")
            return self._state

    def consume(self) -> InterruptState:
        with self._lock:
            current = self._state
            self._state = InterruptState(False, "")
            return current

    def is_interrupted(self) -> bool:
        with self._lock:
            return self._state.interrupted
