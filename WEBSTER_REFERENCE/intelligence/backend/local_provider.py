"""Local-first AI provider with deterministic intelligence routing."""
from __future__ import annotations

import re

from .decision_engine import ProviderResponse
from .intent_pipeline import IntelligencePipeline
from .local_calculator import calculate
from .local_knowledge import LocalKnowledge
from ..ai.local_ai_controller import LocalAIController


class LocalProvider:
    """Dependency-free provider that uses WEBSTER's local intelligence pipeline."""

    name = "local"

    def __init__(self) -> None:
        self.knowledge = LocalKnowledge()
        self.intelligence = IntelligencePipeline()
        self.local_ai = LocalAIController()

    def generate(self, prompt: str) -> ProviderResponse:
        cleaned = " ".join(prompt.split())
        if not cleaned:
            return ProviderResponse("Tell me what you need.", self.name, 1.0, (("mode", "local"),))

        interpretation = self.intelligence.interpret(cleaned)
        known = self.knowledge.answer(cleaned)
        if known:
            return ProviderResponse(
                known, self.name, 0.96,
                (("mode", "local"), ("source", "builtin"), ("intent", interpretation.intent)),
            )

        expression = re.sub(r"^(what is|calculate|compute|solve)\s+", "", cleaned, flags=re.I).rstrip("?")
        if re.fullmatch(r"[\d\s+\-*/%().×÷]+", expression):
            value = calculate(expression)
            if value is not None:
                return ProviderResponse(
                    f"The answer is {value}.", self.name, 0.99,
                    (("mode", "local"), ("source", "calculator"), ("intent", interpretation.intent)),
                )

        try:
            generated = self.local_ai.generate(cleaned, profile="eco")
            if generated.text and not generated.text.startswith("Local model runtime received:"):
                return ProviderResponse(generated.text, self.name, generated.confidence, (("mode", "local-model"), ("model", generated.model_id)))
        except Exception:
            pass

        if not interpretation.constraints_allowed:
            return ProviderResponse(
                "I understood the request, but one or more constraints blocked this operation.",
                self.name, 0.90,
                (("mode", "local"), ("source", "constraint"), ("intent", interpretation.intent)),
            )

        if cleaned.endswith("?"):
            return ProviderResponse(
                "I understood this as a question, but my local knowledge does not contain enough information to answer it yet.",
                self.name, 0.62,
                (("mode", "local"), ("source", "knowledge_gap"), ("intent", interpretation.intent)),
            )
        return ProviderResponse(
            f"I understood this as {interpretation.intent} and routed it to {interpretation.target}.",
            self.name, 0.78,
            (("mode", "local"), ("source", "intent"), ("intent", interpretation.intent), ("target", interpretation.target)),
        )
