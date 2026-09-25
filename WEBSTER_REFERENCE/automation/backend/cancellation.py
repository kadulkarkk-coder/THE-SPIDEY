"""Cooperative cancellation registry for automation tasks."""
from __future__ import annotations

class CancellationRegistry:
    def __init__(self) -> None: self._cancelled: set[str] = set()
    def cancel(self, task_id: str) -> None: self._cancelled.add(task_id.strip())
    def clear(self, task_id: str) -> None: self._cancelled.discard(task_id.strip())
    def is_cancelled(self, task_id: str) -> bool: return task_id.strip() in self._cancelled
