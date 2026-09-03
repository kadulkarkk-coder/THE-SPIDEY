"""Deterministic priority scoring for WEBSTER tasks and goals."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PriorityItem:
    """A schedulable item with normalized priority inputs."""
    name: str
    urgency: float = 0.0
    importance: float = 0.0
    effort: float = 0.0
    deadline_pressure: float = 0.0

    def score(self) -> float:
        urgency = max(0.0, min(1.0, self.urgency))
        importance = max(0.0, min(1.0, self.importance))
        effort = max(0.0, min(1.0, self.effort))
        deadline = max(0.0, min(1.0, self.deadline_pressure))
        return round((0.35 * importance) + (0.30 * urgency) + (0.25 * deadline) + (0.10 * (1.0 - effort)), 4)


class PriorityEngine:
    """Ranks work using transparent, bounded scoring rather than opaque heuristics."""

    def score(self, item: PriorityItem) -> float:
        return item.score()

    def rank(self, items: list[PriorityItem]) -> tuple[PriorityItem, ...]:
        return tuple(sorted(items, key=self.score, reverse=True))
