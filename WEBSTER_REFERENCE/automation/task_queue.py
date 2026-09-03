"""Bounded in-memory queue for automation tasks."""
from __future__ import annotations
from dataclasses import dataclass
from collections import deque

@dataclass(frozen=True)
class AutomationTask:
    task_id: str
    workflow: str
    payload: object = None
    priority: int = 0

class TaskQueue:
    def __init__(self, max_size: int = 100) -> None:
        self.max_size = max(1, max_size)
        self._queue: deque[AutomationTask] = deque()

    def submit(self, task: AutomationTask) -> None:
        if not task.task_id.strip() or not task.workflow.strip(): raise ValueError("task_id and workflow are required")
        if len(self._queue) >= self.max_size: raise OverflowError("automation task queue is full")
        self._queue.append(task)

    def next(self) -> AutomationTask | None:
        if not self._queue: return None
        best = max(range(len(self._queue)), key=lambda i: self._queue[i].priority)
        self._queue.rotate(-best)
        item = self._queue.popleft()
        self._queue.rotate(best)
        return item

    def size(self) -> int: return len(self._queue)
