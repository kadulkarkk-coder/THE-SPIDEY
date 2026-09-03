"""Lightweight delayed scheduling for automation tasks."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
import heapq

@dataclass(frozen=True)
class ScheduledTask:
    task_id: str
    workflow: str
    run_at: datetime
    payload: object = None

class AutomationScheduler:
    def __init__(self) -> None: self._items: list[tuple[float, int, ScheduledTask]] = []; self._seq = 0
    def schedule(self, task: ScheduledTask) -> None:
        self._seq += 1
        when = task.run_at.timestamp()
        heapq.heappush(self._items, (when, self._seq, task))
    def ready(self, now: datetime | None = None) -> tuple[ScheduledTask, ...]:
        current = (now or datetime.now(timezone.utc)).timestamp()
        ready = []
        while self._items and self._items[0][0] <= current: ready.append(heapq.heappop(self._items)[2])
        return tuple(ready)
    def size(self) -> int: return len(self._items)
