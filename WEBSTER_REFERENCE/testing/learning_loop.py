"""Deterministic local learning loop for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass
from .failure_patterns import FailurePatternDetector
from .improvement_candidates import ImprovementCandidate, ImprovementCandidateBuilder
from .learning_records import LearningRecord, LearningStore
from .performance_analyzer import PerformanceAnalyzer, PerformanceSnapshot


@dataclass(frozen=True)
class LearningCycle:
    performance: PerformanceSnapshot
    patterns: tuple[tuple[str, int], ...]
    candidates: tuple[ImprovementCandidate, ...]


class LocalLearningLoop:
    """Observe and propose improvements; it never modifies WEBSTER automatically."""

    def __init__(self, store: LearningStore | None = None) -> None:
        self.store = store or LearningStore()
        self.performance = PerformanceAnalyzer()
        self.patterns = FailurePatternDetector()
        self.candidates = ImprovementCandidateBuilder()

    def record(self, record: LearningRecord) -> None:
        self.store.add(record)

    def analyze(self) -> LearningCycle:
        records = self.store.records()
        patterns = self.patterns.detect(records)
        return LearningCycle(self.performance.analyze(records), patterns, self.candidates.build(patterns))
