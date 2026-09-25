"""High-level deterministic intelligence pipeline for WEBSTER."""
from __future__ import annotations
from dataclasses import dataclass
from .reasoning_engine import ReasoningEngine
from .decision_engine import DecisionEngine, Decision
from .uncertainty_engine import UncertaintyEngine
from .response_policy import ResponsePolicy

@dataclass(frozen=True)
class IntelligenceResult:
    interpretation: object
    decision: Decision
    response_mode: str
    uncertainty: float

class IntelligencePipeline:
    def __init__(self, reasoning=None, decision=None) -> None:
        self.reasoning = reasoning or ReasoningEngine()
        self.decision = decision or DecisionEngine()
        self.uncertainty = UncertaintyEngine()
        self.policy = ResponsePolicy()

    def process(self, text: str) -> IntelligenceResult:
        interpretation = self.reasoning.analyze(text)
        decision = self.decision.decide(text)
        uncertainty = self.uncertainty.assess(confidence=decision.confidence, ambiguity=0.0).score
        mode = self.policy.choose(confidence=decision.confidence, uncertainty=uncertainty)
        return IntelligenceResult(interpretation, decision, mode, uncertainty)
