"""Low-overhead metrics for gesture processing."""
from __future__ import annotations

from dataclasses import dataclass
from threading import Lock


@dataclass(frozen=True)
class GestureMetricsSnapshot:
    processed: int
    accepted: int
    rejected: int

    @property
    def acceptance_rate(self) -> float:
        return self.accepted / self.processed if self.processed else 0.0


class GestureMetrics:
    """Thread-safe counters with constant-size memory usage."""

    def __init__(self) -> None:
        self._processed = 0
        self._accepted = 0
        self._rejected = 0
        self._lock = Lock()

    def record(self, accepted: bool) -> None:
        with self._lock:
            self._processed += 1
            if accepted:
                self._accepted += 1
            else:
                self._rejected += 1

    def snapshot(self) -> GestureMetricsSnapshot:
        with self._lock:
            return GestureMetricsSnapshot(self._processed, self._accepted, self._rejected)

    def reset(self) -> None:
        with self._lock:
            self._processed = self._accepted = self._rejected = 0
