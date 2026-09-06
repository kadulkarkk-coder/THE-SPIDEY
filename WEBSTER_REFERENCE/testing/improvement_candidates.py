"""Create conservative improvement candidates from measured failures."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ImprovementCandidate:
    area: str
    reason: str
    priority: float = 0.0
    reversible: bool = True


class ImprovementCandidateBuilder:
    """Convert repeated failure signals into reviewable, non-mutating candidates."""

    def build(self, patterns: tuple[tuple[str, int], ...]) -> tuple[ImprovementCandidate, ...]:
        candidates = [
            ImprovementCandidate(area, f"repeated failures: {count}", min(1.0, count / 10.0))
            for area, count in patterns
        ]
        return tuple(sorted(candidates, key=lambda item: (-item.priority, item.area)))
