"""Health state derived from recent tool observations."""
from __future__ import annotations
from dataclasses import dataclass
from .tool_observer import ToolObserver

@dataclass(frozen=True)
class ToolHealth:
    calls: int
    failures: int
    success_rate: float

class ToolHealthMonitor:
    def assess(self, tool: str, observer: ToolObserver, limit: int = 20) -> ToolHealth:
        records = tuple(x for x in observer.recent(limit) if x.tool == tool.strip().lower())
        failures = sum(not x.success for x in records)
        rate = 1.0 if not records else (len(records) - failures) / len(records)
        return ToolHealth(len(records), failures, round(rate, 4))
