"""Observable metrics for automation execution."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class AutomationMetrics:
    submitted: int = 0
    completed: int = 0
    failed: int = 0
    cancelled: int = 0

class AutomationMetricsCollector:
    def collect(self, events) -> AutomationMetrics:
        counts = {"submitted": 0, "completed": 0, "failed": 0, "cancelled": 0}
        for event in events:
            if getattr(event, "event", "") in counts: counts[event.event] += 1
        return AutomationMetrics(**counts)
