"""Lightweight intent statistics for improving routing over time."""
from __future__ import annotations
from collections import Counter

class IntentMemory:
    def __init__(self) -> None:
        self._counts: Counter[str] = Counter()

    def record(self, intent: str) -> None:
        intent = intent.strip().lower()
        if intent: self._counts[intent] += 1

    def count(self, intent: str) -> int:
        return self._counts[intent.strip().lower()]

    def frequent(self, limit: int = 5) -> tuple[tuple[str, int], ...]:
        return tuple(self._counts.most_common(max(0, limit)))
