"""Observable execution records for the tool framework."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class ToolObservation:
    tool: str
    success: bool
    duration_ms: float
    timestamp: datetime

class ToolObserver:
    def __init__(self) -> None:
        self._records: list[ToolObservation] = []

    def record(self, tool: str, success: bool, duration_ms: float) -> ToolObservation:
        if duration_ms < 0: raise ValueError("duration_ms must be non-negative")
        item = ToolObservation(tool.strip().lower(), bool(success), float(duration_ms), datetime.now(timezone.utc))
        self._records.append(item)
        return item

    def recent(self, limit: int = 20) -> tuple[ToolObservation, ...]:
        return tuple(self._records[-max(1, limit):])
