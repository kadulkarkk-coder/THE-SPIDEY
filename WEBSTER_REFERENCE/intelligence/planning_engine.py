"""Explicit goal-to-plan decomposition for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlanStep:
    index: int
    description: str
    status: str = "pending"


@dataclass(frozen=True)
class Plan:
    goal: str
    steps: tuple[PlanStep, ...]


class PlanningEngine:
    """Creates deterministic, inspectable plans without executing them."""

    def create_plan(self, goal: str) -> Plan:
        cleaned = " ".join(goal.split())
        if not cleaned:
            return Plan("", ())
        parts = [part.strip() for part in cleaned.replace(" then ", "\n").splitlines() if part.strip()]
        if not parts:
            parts = [cleaned]
        steps = tuple(PlanStep(i, part) for i, part in enumerate(parts, start=1))
        return Plan(cleaned, steps)

    @staticmethod
    def mark_step(plan: Plan, index: int, status: str) -> Plan:
        allowed = {"pending", "active", "completed", "failed", "skipped"}
        if status not in allowed:
            raise ValueError(f"Unsupported step status: {status}")
        steps = tuple(
            PlanStep(step.index, step.description, status if step.index == index else step.status)
            for step in plan.steps
        )
        return Plan(plan.goal, steps)
