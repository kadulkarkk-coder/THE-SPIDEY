"""Simple deterministic scheduler for ready agent tasks."""
from __future__ import annotations
from dataclasses import dataclass
import heapq

@dataclass(frozen=True)
class AgentTask:
    task_id: str
    agent: str
    priority: int = 0

class AgentScheduler:
    def __init__(self): self._queue: list[tuple[int, int, AgentTask]] = []; self._seq = 0
    def submit(self, task: AgentTask) -> None:
        self._seq += 1; heapq.heappush(self._queue, (-task.priority, self._seq, task))
    def next(self) -> AgentTask | None:
        return heapq.heappop(self._queue)[2] if self._queue else None
    def size(self) -> int: return len(self._queue)
