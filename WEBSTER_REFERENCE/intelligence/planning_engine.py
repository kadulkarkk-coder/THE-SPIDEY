"""Explicit goal-to-plan decomposition for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlanStep:
    index: int
    description: str
    status: str = "pending"
    depends_on: tuple[int, ...] = ()


@dataclass(frozen=True)
class Plan:
    goal: str
    steps: tuple[PlanStep, ...]

    @property
    def completed(self) -> int:
        return sum(step.status == "completed" for step in self.steps)

    @property
    def progress(self) -> float:
        return self.completed / len(self.steps) if self.steps else 0.0


class PlanningEngine:
    """Creates deterministic, inspectable plans without executing them."""

    def create_plan(self, goal: str) -> Plan:
        cleaned = " ".join(goal.split())
        if not cleaned:
            return Plan("", ())
        parts = [part.strip() for part in cleaned.replace(" then ", "\n").splitlines() if part.strip()]
        if not parts:
            parts = [cleaned]
        steps = tuple(
            PlanStep(i, part, "pending", (i - 1,) if i > 1 else ())
            for i, part in enumerate(parts, start=1)
        )
        return Plan(cleaned, steps)

    @staticmethod
    def mark_step(plan: Plan, index: int, status: str) -> Plan:
        allowed = {"pending", "active", "completed", "failed", "skipped"}
        if status not in allowed:
            raise ValueError(f"Unsupported step status: {status}")
        if index not in {step.index for step in plan.steps}:
            raise IndexError(f"Unknown plan step: {index}")
        steps = tuple(
            PlanStep(step.index, step.description, status if step.index == index else step.status, step.depends_on)
            for step in plan.steps
        )
        return Plan(plan.goal, steps)

    @staticmethod
    def next_ready(plan: Plan) -> tuple[PlanStep, ...]:
        completed = {step.index for step in plan.steps if step.status == "completed"}
        return tuple(
            step for step in plan.steps
            if step.status == "pending" and all(dep in completed for dep in step.depends_on)
        )
