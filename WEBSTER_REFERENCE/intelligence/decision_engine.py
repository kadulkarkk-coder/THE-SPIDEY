"""AI provider and decision boundary for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ProviderResponse:
    text: str
    provider: str
    confidence: float = 0.0
    metadata: tuple[tuple[str, str], ...] = ()


class AIProvider(Protocol):
    name: str

    def generate(self, prompt: str) -> ProviderResponse:
        """Generate a provider response."""


class OfflineProvider:
    name = "offline"

    def generate(self, prompt: str) -> ProviderResponse:
        cleaned = " ".join(prompt.split())
        if not cleaned:
            return ProviderResponse("No input provided.", self.name, 1.0)
        return ProviderResponse(
            f"Offline provider received: {cleaned}", self.name, 0.35,
            (("mode", "fallback"),),
        )


@dataclass(frozen=True)
class Decision:
    action: str
    confidence: float
    provider: str
    rationale: str
    requires_review: bool = False


class DecisionEngine:
    """Turns provider output into an inspectable, conservative decision."""

    def __init__(self, provider: AIProvider | None = None, *, review_threshold: float = 0.5) -> None:
        if not 0.0 <= review_threshold <= 1.0:
            raise ValueError("review_threshold must be between 0 and 1")
        self.provider = provider or OfflineProvider()
        self.review_threshold = review_threshold

    def decide(self, prompt: str) -> Decision:
        response = self.provider.generate(prompt)
        confidence = max(0.0, min(1.0, response.confidence))
        action = "respond" if response.text else "wait"
        return Decision(
            action=action,
            confidence=confidence,
            provider=response.provider,
            rationale=response.text,
            requires_review=confidence < self.review_threshold,
        )
