"""Structured reasoning boundary for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass
from .intent_detection import IntentResult, detect_intent
from .entity_extraction import EntityResult, extract_entities


@dataclass(frozen=True)
class ReasoningResult:
    intent: IntentResult
    entities: EntityResult
    goal: str


class ReasoningEngine:
    """Produces an inspectable interpretation without exposing hidden reasoning."""

    def analyze(self, text: str) -> ReasoningResult:
        cleaned = " ".join(text.split())
        intent = detect_intent(cleaned)
        entities = extract_entities(cleaned)
        return ReasoningResult(intent=intent, entities=entities, goal=cleaned)
