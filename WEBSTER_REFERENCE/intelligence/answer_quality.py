"""Deterministic answer-quality scoring for WEBSTER."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class QualityScore:
    score: float
    label: str

class AnswerQualityEvaluator:
    def evaluate(self, *, relevance: float, completeness: float, confidence: float) -> QualityScore:
        values = [max(0.0, min(1.0, v)) for v in (relevance, completeness, confidence)]
        score = round(sum(values) / 3, 4)
        label = "high" if score >= 0.8 else "medium" if score >= 0.5 else "low"
        return QualityScore(score, label)
