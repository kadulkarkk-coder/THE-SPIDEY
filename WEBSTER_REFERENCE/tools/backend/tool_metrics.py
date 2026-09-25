"""Observable counters for tool selection and execution outcomes."""
from __future__ import annotations
from dataclasses import dataclass
from threading import RLock

@dataclass(frozen=True)
class ToolMetrics:
    calls: int
    successes: int
    failures: int

class ToolMetricsCollector:
    def __init__(self) -> None:
        self._calls = 0
        self._successes = 0
        self._failures = 0
        self._lock = RLock()

    def record(self, success: bool) -> None:
        with self._lock:
            self._calls += 1
            if success: self._successes += 1
            else: self._failures += 1

    def snapshot(self) -> ToolMetrics:
        with self._lock:
            return ToolMetrics(self._calls, self._successes, self._failures)
