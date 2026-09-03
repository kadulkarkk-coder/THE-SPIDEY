"""Safe answer synthesis from structured inputs."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SynthesizedAnswer:
    text: str
    confidence: float
    sources: tuple[str, ...]


class AnswerSynthesizer:
    """Combines candidate text and evidence without pretending certainty."""

    def synthesize(self, candidates: tuple[str, ...], confidence: float = 0.5,
                   sources: tuple[str, ...] = ()) -> SynthesizedAnswer:
        usable = tuple(" ".join(item.split()) for item in candidates if item and item.strip())
        if not usable:
            return SynthesizedAnswer("I don't have enough information to answer yet.", 0.0, tuple(sources))
        confidence = max(0.0, min(1.0, confidence))
        text = usable[0] if len(usable) == 1 else " ".join(usable)
        return SynthesizedAnswer(text, confidence, tuple(sources))
