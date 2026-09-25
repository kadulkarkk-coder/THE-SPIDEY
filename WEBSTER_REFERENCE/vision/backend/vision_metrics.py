"""Lightweight metrics for the WEBSTER vision subsystem."""
from __future__ import annotations
from dataclasses import dataclass
from threading import RLock


@dataclass(frozen=True)
class VisionMetricsSnapshot:
    total: int
    successful: int
    failed: int

    @property
    def success_rate(self) -> float:
        return self.successful / self.total if self.total else 0.0


class VisionMetrics:
    """Thread-safe counters with no dependency on a telemetry service."""

    def __init__(self) -> None:
        self._total = 0
        self._successful = 0
        self._failed = 0
        self._lock = RLock()

    def record(self, success: bool) -> VisionMetricsSnapshot:
        with self._lock:
            self._total += 1
            if success:
                self._successful += 1
            else:
                self._failed += 1
            return self.snapshot()

    def snapshot(self) -> VisionMetricsSnapshot:
        with self._lock:
            return VisionMetricsSnapshot(self._total, self._successful, self._failed)

    def reset(self) -> None:
        with self._lock:
            self._total = self._successful = self._failed = 0
