"""Explicit fact storage with source and confidence metadata."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class Fact:
    subject: str
    predicate: str
    value: str
    source: str = "unknown"
    confidence: float = 1.0
    recorded_at: datetime = None

class FactStore:
    def __init__(self) -> None:
        self._facts: list[Fact] = []

    def add(self, subject: str, predicate: str, value: str, *, source: str = "unknown", confidence: float = 1.0) -> Fact:
        fact = Fact(subject.strip(), predicate.strip(), value.strip(), source.strip(), max(0.0, min(1.0, confidence)), datetime.now(timezone.utc))
        self._facts.append(fact)
        return fact

    def find(self, subject: str, predicate: str | None = None) -> tuple[Fact, ...]:
        return tuple(f for f in self._facts if f.subject == subject and (predicate is None or f.predicate == predicate))
