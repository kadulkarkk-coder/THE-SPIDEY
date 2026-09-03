"""Goal lifecycle management for WEBSTER intelligence."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class GoalState(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Goal:
    """A user objective with explicit lifecycle state and constraints."""
    text: str
    id: str = field(default_factory=lambda: uuid4().hex)
    state: GoalState = GoalState.PENDING
    constraints: tuple[str, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)

    def activate(self) -> None:
        if self.state is GoalState.PENDING:
            self.state = GoalState.ACTIVE

    def complete(self) -> None:
        if self.state in (GoalState.PENDING, GoalState.ACTIVE):
            self.state = GoalState.COMPLETED

    def fail(self) -> None:
        if self.state in (GoalState.PENDING, GoalState.ACTIVE):
            self.state = GoalState.FAILED

    def cancel(self) -> None:
        if self.state in (GoalState.PENDING, GoalState.ACTIVE):
            self.state = GoalState.CANCELLED


class GoalManager:
    """Stores goals in memory and enforces simple lifecycle transitions."""

    def __init__(self) -> None:
        self._goals: dict[str, Goal] = {}

    def create(self, text: str, *, constraints: tuple[str, ...] = ()) -> Goal:
        cleaned = " ".join(text.split())
        if not cleaned:
            raise ValueError("Goal cannot be empty")
        goal = Goal(cleaned, constraints=tuple(c for c in constraints if c.strip()))
        self._goals[goal.id] = goal
        return goal

    def get(self, goal_id: str) -> Goal | None:
        return self._goals.get(goal_id)

    def active(self) -> tuple[Goal, ...]:
        return tuple(g for g in self._goals.values() if g.state is GoalState.ACTIVE)

    def all(self) -> tuple[Goal, ...]:
        return tuple(self._goals.values())
