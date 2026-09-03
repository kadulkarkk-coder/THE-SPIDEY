"""High-level, deterministic pipeline for controlled tool execution."""
from __future__ import annotations
from dataclasses import dataclass
from time import perf_counter
from typing import Any, Callable
from .tool_budget import ToolBudget
from .tool_observer import ToolObserver
from .tool_transaction import ToolTransaction

@dataclass(frozen=True)
class ToolPipelineResult:
    success: bool
    value: Any = None
    error: str | None = None
    duration_ms: float = 0.0

class ToolPipeline:
    def __init__(self, observer: ToolObserver | None = None) -> None:
        self.observer = observer or ToolObserver()
        self.transaction = ToolTransaction()

    def execute(self, tool: str, action: Callable[[], Any], *, budget: ToolBudget | None = None, cost: float = 1.0, rollback: Callable[[], None] | None = None) -> ToolPipelineResult:
        if budget is not None and not budget.consume(cost):
            result = ToolPipelineResult(False, error="tool execution budget exceeded")
            self.observer.record(tool, False, 0.0)
            return result
        started = perf_counter()
        tx = self.transaction.run(action, rollback)
        duration = (perf_counter() - started) * 1000.0
        self.observer.record(tool, tx.success, duration)
        return ToolPipelineResult(tx.success, tx.value, tx.error, round(duration, 3))
