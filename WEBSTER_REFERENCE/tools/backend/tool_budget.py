"""Bound execution budgets for tool calls."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ToolBudget:
    max_calls: int = 10
    max_cost: float = 10.0
    calls: int = 0
    cost: float = 0.0

    def consume(self, cost: float = 1.0) -> bool:
        if cost < 0: raise ValueError("cost must be non-negative")
        if self.calls >= max(0, self.max_calls) or self.cost + cost > max(0.0, self.max_cost):
            return False
        self.calls += 1
        self.cost += cost
        return True

    def remaining_calls(self) -> int:
        return max(0, self.max_calls - self.calls)

    def remaining_cost(self) -> float:
        return max(0.0, self.max_cost - self.cost)
