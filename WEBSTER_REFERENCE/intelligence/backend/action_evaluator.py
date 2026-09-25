"""Pre-action evaluation for WEBSTER plans."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ActionEvaluation:
    allowed: bool
    confidence: float
    reasons: tuple[str, ...] = ()

class ActionEvaluator:
    def evaluate(self, *, confidence: float, risk: float = 0.0, requires_confirmation: bool = False) -> ActionEvaluation:
        confidence = max(0.0, min(1.0, confidence))
        risk = max(0.0, min(1.0, risk))
        reasons: list[str] = []
        if confidence < 0.5: reasons.append("low_confidence")
        if risk >= 0.8: reasons.append("high_risk")
        if requires_confirmation: reasons.append("confirmation_required")
        return ActionEvaluation(not reasons, confidence, tuple(reasons))
