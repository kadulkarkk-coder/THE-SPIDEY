"""Auditable records for intelligence decisions."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class DecisionAudit:
    action: str
    confidence: float
    outcome: str
    timestamp: datetime

class DecisionAuditor:
    def record(self, action: str, confidence: float, outcome: str) -> DecisionAudit:
        return DecisionAudit(action.strip(), max(0.0, min(1.0, confidence)), outcome.strip(), datetime.now(timezone.utc))
