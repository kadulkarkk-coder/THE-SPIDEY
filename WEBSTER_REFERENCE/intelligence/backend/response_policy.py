"""Response policy selection for WEBSTER."""
from __future__ import annotations

class ResponsePolicy:
    def choose(self, *, confidence: float, uncertainty: float = 0.0) -> str:
        confidence = max(0.0, min(1.0, confidence))
        uncertainty = max(0.0, min(1.0, uncertainty))
        if uncertainty >= 0.7 or confidence < 0.4:
            return "clarify"
        if uncertainty >= 0.4 or confidence < 0.7:
            return "qualified"
        return "direct"
