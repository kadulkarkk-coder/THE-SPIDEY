"""Runtime diagnostics and request metrics for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from time import monotonic
from typing import Any


@dataclass(frozen=True)
class DiagnosticSnapshot:
    requests: int
    successes: int
    failures: int
    total_duration_ms: float

    @property
    def success_rate(self) -> float:
        return self.successes / self.requests if self.requests else 1.0


class Diagnostics:
    """Collect lightweight metrics without external dependencies."""

    def __init__(self) -> None:
        self._requests = 0
        self._successes = 0
        self._failures = 0
        self._duration = 0.0
        self._lock = RLock()

    def record(self, *, ok: bool, started_at: float) -> None:
        elapsed_ms = max(0.0, (monotonic() - started_at) * 1000.0)
        with self._lock:
            self._requests += 1
            self._successes += int(ok)
            self._failures += int(not ok)
            self._duration += elapsed_ms

    def snapshot(self) -> DiagnosticSnapshot:
        with self._lock:
            return DiagnosticSnapshot(self._requests, self._successes, self._failures, self._duration)

    def as_dict(self) -> dict[str, Any]:
        snapshot = self.snapshot()
        return {
            "requests": snapshot.requests,
            "successes": snapshot.successes,
            "failures": snapshot.failures,
            "success_rate": snapshot.success_rate,
            "total_duration_ms": round(snapshot.total_duration_ms, 3),
        }

    def reset(self) -> None:
        with self._lock:
            self._requests = self._successes = self._failures = 0
            self._duration = 0.0
