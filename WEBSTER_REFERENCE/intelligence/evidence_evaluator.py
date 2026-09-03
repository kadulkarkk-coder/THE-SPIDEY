"""Lightweight evidence scoring for inspectable decisions."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    source: str
    relevance: float
    reliability: float

    @property
    def score(self) -> float:
        return self.relevance * self.reliability


class EvidenceEvaluator:
    def evaluate(self, source: str, relevance: float, reliability: float) -> Evidence:
        source = source.strip()
        if not source:
            raise ValueError("source is required")
        if not 0.0 <= relevance <= 1.0 or not 0.0 <= reliability <= 1.0:
            raise ValueError("relevance and reliability must be between 0 and 1")
        return Evidence(source, relevance, reliability)

    @staticmethod
    def combined(evidence: tuple[Evidence, ...]) -> float:
        if not evidence:
            return 0.0
        return min(1.0, sum(item.score for item in evidence) / len(evidence))
