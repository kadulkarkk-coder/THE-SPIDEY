"""Pre-action risk assessment for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskAssessment:
    level: str
    score: float
    reasons: tuple[str, ...]


class RiskAssessor:
    """Classifies proposed actions before execution."""

    HIGH_RISK_TERMS = ("delete", "remove", "send", "publish", "install", "shutdown")
    MEDIUM_RISK_TERMS = ("modify", "write", "move", "rename")

    def assess(self, action: str) -> RiskAssessment:
        text = " ".join(action.lower().split())
        reasons = []
        if any(term in text for term in self.HIGH_RISK_TERMS):
            reasons.append("action can cause an external or destructive effect")
            return RiskAssessment("high", 0.85, tuple(reasons))
        if any(term in text for term in self.MEDIUM_RISK_TERMS):
            reasons.append("action changes persistent state")
            return RiskAssessment("medium", 0.5, tuple(reasons))
        return RiskAssessment("low", 0.1, ())
