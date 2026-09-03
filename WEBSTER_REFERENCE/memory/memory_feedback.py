"""Feedback signals for improving memory retrieval without self-modifying code."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class MemoryFeedback:
    record_id: str
    useful: bool
    signal: float

class MemoryFeedbackTracker:
    def __init__(self) -> None:
        self._signals: list[MemoryFeedback] = []

    def record(self, record_id: str, useful: bool) -> MemoryFeedback:
        feedback = MemoryFeedback(record_id.strip(), useful, 1.0 if useful else -1.0)
        if not feedback.record_id: raise ValueError("record_id is required")
        self._signals.append(feedback)
        return feedback

    def score(self, record_id: str) -> float:
        values = [f.signal for f in self._signals if f.record_id == record_id.strip()]
        return round(sum(values) / len(values), 4) if values else 0.0
