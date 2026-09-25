"""Deterministic semantic routing for WEBSTER requests."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Route:
    name: str
    confidence: float
    matched_terms: tuple[str, ...]


class SemanticRouter:
    """Routes requests to capability families without requiring an online model."""

    RULES = {
        "knowledge": ("what", "why", "who", "explain", "meaning", "define"),
        "planning": ("plan", "schedule", "organize", "steps", "roadmap"),
        "automation": ("automate", "repeat", "workflow", "every day", "remind"),
        "system": ("open", "close", "launch", "file", "folder", "computer"),
        "browser": ("website", "web", "browser", "search", "url", "page"),
        "conversation": ("hello", "hi", "thanks", "remember", "tell me"),
    }

    def route(self, text: str) -> Route:
        cleaned = " ".join(text.lower().split())
        if not cleaned:
            return Route("unknown", 0.0, ())
        scores = {
            name: tuple(term for term in terms if term in cleaned)
            for name, terms in self.RULES.items()
        }
        ranked = sorted(scores.items(), key=lambda item: len(item[1]), reverse=True)
        name, matches = ranked[0]
        if not matches:
            return Route("general", 0.2, ())
        confidence = min(0.95, 0.45 + 0.15 * len(matches))
        return Route(name, confidence, matches)
