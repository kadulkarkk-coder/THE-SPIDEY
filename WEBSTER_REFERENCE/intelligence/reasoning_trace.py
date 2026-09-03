"""Public, compact reasoning trace for observability and debugging."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class ReasoningTrace:
    stage: str
    summary: str
    timestamp: datetime


class ReasoningTraceRecorder:
    """Records concise reasoning events without exposing hidden chain-of-thought."""

    def __init__(self, limit: int = 100) -> None:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        self.limit = limit
        self._items: list[ReasoningTrace] = []

    def record(self, stage: str, summary: str) -> ReasoningTrace:
        stage = stage.strip().lower()
        summary = " ".join(summary.split())
        if not stage or not summary:
            raise ValueError("stage and summary are required")
        trace = ReasoningTrace(stage, summary, datetime.now(timezone.utc))
        self._items.append(trace)
        del self._items[:-self.limit]
        return trace

    def recent(self, limit: int | None = None) -> tuple[ReasoningTrace, ...]:
        if limit is None:
            limit = self.limit
        if limit < 1:
            return ()
        return tuple(self._items[-limit:])
