"""Functional intent/reasoning pipeline for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .constraint_engine import Constraint, ConstraintEngine
from .intent_router import IntentRoute, IntentRouter


@dataclass(frozen=True)
class IntelligenceInterpretation:
    text: str
    intent: str
    confidence: float
    target: str
    entities: tuple[dict[str, str], ...]
    goal: str
    constraints_allowed: bool
    failed_constraints: tuple[str, ...]
    route_reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "intent": self.intent,
            "confidence": self.confidence,
            "target": self.target,
            "entities": list(self.entities),
            "goal": self.goal,
            "constraints_allowed": self.constraints_allowed,
            "failed_constraints": list(self.failed_constraints),
            "route_reason": self.route_reason,
        }


class IntelligencePipeline:
    """UNDERSTAND -> REASON -> CONSTRAIN -> ROUTE, without executing actions."""

    def __init__(self, router: IntentRouter | None = None, constraints: ConstraintEngine | None = None) -> None:
        self.router = router or IntentRouter()
        self.constraints = constraints or ConstraintEngine()

    def interpret(self, text: str, *, constraints: list[Constraint] | None = None) -> IntelligenceInterpretation:
        cleaned = " ".join(text.split())
        reasoning, route = self.router.route(cleaned)
        constraint_result = self.constraints.evaluate(cleaned, constraints or [])
        entities = tuple({"kind": e.kind, "value": e.value} for e in reasoning.entities.entities)
        return IntelligenceInterpretation(
            text=cleaned,
            intent=reasoning.intent.intent,
            confidence=reasoning.intent.confidence,
            target=route.target,
            entities=entities,
            goal=reasoning.goal,
            constraints_allowed=constraint_result.allowed,
            failed_constraints=constraint_result.failed,
            route_reason=route.reason,
        )
