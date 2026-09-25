"""Detect repeated failure categories without retaining sensitive payloads."""
from __future__ import annotations

from collections import Counter
from .learning_records import LearningRecord


class FailurePatternDetector:
    """Identify recurring failure labels from bounded learning records."""

    def detect(self, records: tuple[LearningRecord, ...], *, minimum: int = 2) -> tuple[tuple[str, int], ...]:
        if minimum < 1:
            raise ValueError("minimum must be positive")
        counts = Counter(
            r.event.strip() or "unknown"
            for r in records
            if r.outcome.strip().lower() in {"failure", "failed", "error"}
        )
        return tuple(sorted((name, count) for name, count in counts.items() if count >= minimum))
