"""Uncertainty tracking for WEBSTER intelligence decisions."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Uncertainty:
    score: float
    reasons: tuple[str, ...] = ()

class UncertaintyEngine:
    def assess(self, *, confidence: float, ambiguity: float = 0.0, evidence_gap: float = 0.0) -> Uncertainty:
        values = [max(0.0, min(1.0, value)) for value in (1.0 - confidence, ambiguity, evidence_gap)]
        score = sum(values) / len(values)
        reasons = tuple(name for name, value in zip(("low_confidence", "ambiguity", "evidence_gap"), values) if value >= 0.5)
        return Uncertainty(score, reasons)
