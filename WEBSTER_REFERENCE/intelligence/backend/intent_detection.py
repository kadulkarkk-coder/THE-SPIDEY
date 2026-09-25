"""Deterministic intent classification boundary for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IntentResult:
    intent: str
    confidence: float
    matched_terms: tuple[str, ...] = ()


_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("greeting", ("hello", "hi", "hey")),
    ("help", ("help", "commands")),
    ("status", ("status", "health")),
    ("question", ("what", "why", "when", "where", "who", "how")),
)


def detect_intent(text: str) -> IntentResult:
    words = {word.strip(".,!?;:").lower() for word in text.split()}
    for intent, terms in _RULES:
        matched = tuple(term for term in terms if term in words)
        if matched:
            return IntentResult(intent, min(1.0, 0.55 + 0.1 * len(matched)), matched)
    return IntentResult("unknown", 0.0)
