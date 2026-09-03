"""Resolve competing memory values using explicit confidence and recency."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class CandidateValue:
    value: object
    confidence: float = 0.5
    recorded_at: datetime = None

class MemoryReconciler:
    def choose(self, candidates: tuple[CandidateValue, ...]) -> CandidateValue | None:
        if not candidates:
            return None
        now = datetime.now(timezone.utc)
        def score(c: CandidateValue) -> tuple[float, float]:
            age = (now - c.recorded_at).total_seconds() if c.recorded_at else 10**9
            return (max(0.0, min(1.0, c.confidence)), -age)
        return max(candidates, key=score)
