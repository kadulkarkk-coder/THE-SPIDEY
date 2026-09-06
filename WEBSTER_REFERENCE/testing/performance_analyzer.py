"""Lightweight performance analysis for WEBSTER's learning loop."""
from __future__ import annotations

from dataclasses import dataclass
from .learning_records import LearningRecord


@dataclass(frozen=True)
class PerformanceSnapshot:
    total: int
    successful: int
    failed: int
    average_score: float

    @property
    def success_rate(self) -> float:
        return self.successful / self.total if self.total else 1.0


class PerformanceAnalyzer:
    """Turn learning records into deterministic performance signals."""

    def analyze(self, records: tuple[LearningRecord, ...]) -> PerformanceSnapshot:
        successful = sum(r.outcome.strip().lower() in {"success", "passed", "ok"} for r in records)
        failed = len(records) - successful
        average = sum(max(0.0, min(1.0, r.score)) for r in records) / len(records) if records else 1.0
        return PerformanceSnapshot(len(records), successful, failed, average)
