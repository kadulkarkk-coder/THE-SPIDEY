"""AI provider and decision boundary for WEBSTER.

Sprint 6 keeps the provider layer dependency-free. External model providers can
implement the protocol later without changing the rest of the intelligence stack.
"""
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
    """Minimal contract every WEBSTER AI provider must satisfy."""

    name: str

    def generate(self, prompt: str) -> ProviderResponse:
        """Generate a response without exposing provider-specific details."""


class OfflineProvider:
    """Deterministic local fallback used when no external model is configured."""

    name = "offline"

    def generate(self, prompt: str) -> ProviderResponse:
        cleaned = " ".join(prompt.split())
        if not cleaned:
            return ProviderResponse("No input provided.", self.name, 1.0)
        return ProviderResponse(
            f"Offline provider received: {cleaned}",
            self.name,
            0.35,
            (("mode", "fallback"),),
        )


@dataclass(frozen=True)
class Decision:
    action: str
    confidence: float
    provider: str
    rationale: str


class DecisionEngine:
    """Turns provider output into a small, inspectable execution decision."""

    def __init__(self, provider: AIProvider | None = None) -> None:
        self.provider = provider or OfflineProvider()

    def decide(self, prompt: str) -> Decision:
        response = self.provider.generate(prompt)
        action = "respond" if response.text else "wait"
        return Decision(
            action=action,
            confidence=response.confidence,
            provider=response.provider,
            rationale=response.text,
        )
