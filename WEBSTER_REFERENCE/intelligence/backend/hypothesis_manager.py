"""Inspectable hypothesis management for uncertain reasoning."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Hypothesis:
    statement: str
    confidence: float
    evidence: tuple[str, ...] = ()


class HypothesisManager:
    """Keeps alternative interpretations explicit instead of silently guessing."""

    def __init__(self) -> None:
        self._items: list[Hypothesis] = []

    def add(self, statement: str, confidence: float, evidence: tuple[str, ...] = ()) -> Hypothesis:
        statement = " ".join(statement.split())
        if not statement:
            raise ValueError("statement is required")
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        item = Hypothesis(statement, confidence, tuple(evidence))
        self._items.append(item)
        return item

    def ranked(self) -> tuple[Hypothesis, ...]:
        return tuple(sorted(self._items, key=lambda item: item.confidence, reverse=True))

    def clear(self) -> None:
        self._items.clear()
