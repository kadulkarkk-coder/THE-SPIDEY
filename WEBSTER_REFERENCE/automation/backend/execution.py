"""Controlled execution boundary for automation workflows."""
from __future__ import annotations
from dataclasses import dataclass
from .workflow import Workflow

@dataclass(frozen=True)
class AutomationExecution:
    task_id: str
    success: bool
    output: object = None
    error: str | None = None

class AutomationExecutor:
    def execute(self, task_id: str, workflow: Workflow, payload: object = None) -> AutomationExecution:
        result = workflow.run(payload)
        return AutomationExecution(task_id.strip(), result.success, result.output, result.error)
