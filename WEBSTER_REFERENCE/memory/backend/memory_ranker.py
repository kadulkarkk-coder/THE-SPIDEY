"""Rank memory candidates by relevance, confidence, and recency."""
from __future__ import annotations
from datetime import datetime, timezone
from .memory_store import MemoryRecord

class MemoryRanker:
    def score(self, relevance: float, confidence: float = 1.0, record: MemoryRecord | None = None) -> float:
        recency = 0.0
        if record:
            age = max(0.0, (datetime.now(timezone.utc) - record.created_at).total_seconds())
            recency = 1.0 / (1.0 + age / 86400.0)
        return round(0.6 * max(0.0, min(1.0, relevance)) + 0.25 * max(0.0, min(1.0, confidence)) + 0.15 * recency, 4)

    def rank(self, candidates: list[tuple[MemoryRecord, float, float]]) -> tuple[MemoryRecord, ...]:
        return tuple(record for record, _, _ in sorted(candidates, key=lambda x: self.score(x[1], x[2], x[0]), reverse=True))
