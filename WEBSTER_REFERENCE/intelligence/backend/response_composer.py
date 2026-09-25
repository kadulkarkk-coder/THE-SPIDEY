"""Structured response composition for the WEBSTER intelligence boundary."""
from __future__ import annotations

from dataclasses import dataclass

from .decision_engine import Decision


@dataclass(frozen=True)
class ComposedResponse:
    """User-facing response plus machine-readable provenance."""

    text: str
    provider: str
    confidence: float
    action: str
    requires_review: bool
    suggestions: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "text": self.text,
            "provider": self.provider,
            "confidence": self.confidence,
            "action": self.action,
            "requires_review": self.requires_review,
            "suggestions": self.suggestions,
        }


class ResponseComposer:
    """Converts a decision into a stable response contract."""

    def compose(self, decision: Decision) -> ComposedResponse:
        suggestions: tuple[str, ...] = ()
        if decision.requires_review:
            suggestions = ("This response has low confidence; ask WEBSTER to clarify if needed.",)
        return ComposedResponse(
            text=decision.rationale,
            provider=decision.provider,
            confidence=decision.confidence,
            action=decision.action,
            requires_review=decision.requires_review,
            suggestions=suggestions,
        )
