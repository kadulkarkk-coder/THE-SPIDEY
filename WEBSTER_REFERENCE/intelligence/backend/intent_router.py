"""Intent-aware routing for the functional WEBSTER intelligence pipeline."""
from __future__ import annotations

from dataclasses import dataclass

from .reasoning_engine import ReasoningEngine, ReasoningResult


@dataclass(frozen=True)
class IntentRoute:
    intent: str
    target: str
    confidence: float
    reason: str


class IntentRouter:
    """Maps structured intent to a safe downstream capability."""

    _ROUTES = {
        "greeting": "conversation",
        "help": "command_help",
        "status": "runtime_status",
        "question": "knowledge",
        "unknown": "conversation",
    }

    def __init__(self, reasoning: ReasoningEngine | None = None) -> None:
        self.reasoning = reasoning or ReasoningEngine()

    def route(self, text: str) -> tuple[ReasoningResult, IntentRoute]:
        result = self.reasoning.analyze(text)
        intent = result.intent.intent
        target = self._ROUTES.get(intent, "conversation")
        route = IntentRoute(
            intent=intent,
            target=target,
            confidence=result.intent.confidence,
            reason="matched terms: " + (", ".join(result.intent.matched_terms) or "none"),
        )
        return result, route
