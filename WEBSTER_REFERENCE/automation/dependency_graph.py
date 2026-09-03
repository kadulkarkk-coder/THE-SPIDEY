"""Explicit dependency graph for workflow tasks."""
from __future__ import annotations
from collections import defaultdict

class DependencyGraph:
    def __init__(self) -> None: self._deps: dict[str, set[str]] = defaultdict(set)
    def add(self, task_id: str, depends_on: str) -> None:
        task_id, depends_on = task_id.strip(), depends_on.strip()
        if not task_id or not depends_on: raise ValueError("task ids are required")
        if task_id == depends_on: raise ValueError("task cannot depend on itself")
        self._deps[task_id].add(depends_on)
    def ready(self, completed: set[str]) -> tuple[str, ...]:
        done = {x.strip() for x in completed}
        return tuple(sorted(task for task, deps in self._deps.items() if task not in done and deps <= done))
    def dependencies(self, task_id: str) -> tuple[str, ...]: return tuple(sorted(self._deps.get(task_id.strip(), ())))
