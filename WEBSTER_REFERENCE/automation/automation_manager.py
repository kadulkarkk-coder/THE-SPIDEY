"""High-level coordinator for safe automation primitives."""
from __future__ import annotations
from .task_queue import TaskQueue, AutomationTask
from .state import AutomationStateStore
from .cancellation import CancellationRegistry
from .approval_gate import ApprovalGate

class AutomationManager:
    def __init__(self, queue: TaskQueue | None = None) -> None:
        self.queue = queue or TaskQueue()
        self.state = AutomationStateStore()
        self.cancellation = CancellationRegistry()
        self.approval = ApprovalGate()

    def submit(self, task: AutomationTask) -> None:
        self.queue.submit(task)
        self.state.set(task.task_id, "queued")

    def cancel(self, task_id: str) -> None:
        self.cancellation.cancel(task_id)
        self.state.set(task_id, "cancelled")

    def next_task(self):
        while (task := self.queue.next()) is not None:
            if self.cancellation.is_cancelled(task.task_id): continue
            self.state.set(task.task_id, "running")
            return task
        return None
