"""Queue remote laptop actions while the target device is offline."""
from __future__ import annotations

from dataclasses import dataclass
from threading import RLock


@dataclass(frozen=True)
class RemoteQueuedAction:
    action_id: str
    command: str
    device_id: str


class RemoteActionQueue:
    """Stores intent only; execution still requires the laptop-side permission layer."""

    def __init__(self, max_items: int = 100) -> None:
        if max_items < 1:
            raise ValueError("max_items must be positive")
        self._max_items = max_items
        self._items: list[RemoteQueuedAction] = []
        self._lock = RLock()

    def enqueue(self, action: RemoteQueuedAction) -> None:
        if not action.command.strip() or not action.device_id.strip():
            raise ValueError("command and device_id must not be empty")
        with self._lock:
            self._items.append(action)
            if len(self._items) > self._max_items:
                del self._items[: len(self._items) - self._max_items]

    def pending(self) -> tuple[RemoteQueuedAction, ...]:
        with self._lock:
            return tuple(self._items)

    def remove(self, action_id: str) -> None:
        with self._lock:
            self._items = [item for item in self._items if item.action_id != action_id]
