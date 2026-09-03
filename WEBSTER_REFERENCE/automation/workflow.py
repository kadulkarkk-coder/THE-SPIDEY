"""Composable automation workflow definition and execution boundary."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class WorkflowStep:
    name: str
    action: Callable[[Any], Any]

@dataclass(frozen=True)
class WorkflowResult:
    success: bool
    output: Any = None
    failed_step: str | None = None
    error: str | None = None

class Workflow:
    def __init__(self, name: str, steps: tuple[WorkflowStep, ...] = ()) -> None:
        if not name.strip(): raise ValueError("workflow name is required")
        self.name = name.strip()
        self.steps = steps

    def add_step(self, step: WorkflowStep) -> "Workflow":
        if not step.name.strip(): raise ValueError("step name is required")
        return Workflow(self.name, self.steps + (step,))

    def run(self, initial: Any = None) -> WorkflowResult:
        value = initial
        for step in self.steps:
            try: value = step.action(value)
            except Exception as exc: return WorkflowResult(False, value, step.name, f"{exc.__class__.__name__}: {exc}")
        return WorkflowResult(True, value)
