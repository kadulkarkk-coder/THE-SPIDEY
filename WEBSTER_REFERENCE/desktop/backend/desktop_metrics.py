"""Lightweight metrics for desktop capability planning and authorization."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class DesktopMetrics:
    planned: int = 0
    permitted: int = 0
    denied: int = 0

class DesktopMetricsCollector:
    def collect(self, observations) -> DesktopMetrics:
        planned = permitted = denied = 0
        for item in observations:
            planned += 1
            if getattr(item, "success", False):
                permitted += 1
            else:
                denied += 1
        return DesktopMetrics(planned, permitted, denied)
