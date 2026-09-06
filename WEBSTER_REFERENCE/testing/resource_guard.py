"""Low-overhead resource and execution guards for WEBSTER tests."""
from __future__ import annotations

from dataclasses import dataclass
from time import monotonic


@dataclass(frozen=True)
class ResourceLimit:
    max_duration_ms: float = 5000.0
    max_items: int = 10000

    def validate(self) -> None:
        if self.max_duration_ms <= 0:
            raise ValueError("max_duration_ms must be positive")
        if self.max_items <= 0:
            raise ValueError("max_items must be positive")


class ResourceGuard:
    """Guard a test operation without spawning workers or sampling hardware."""

    def __init__(self, limit: ResourceLimit | None = None) -> None:
        self.limit = limit or ResourceLimit()
        self.limit.validate()
        self._started = monotonic()
        self._items = 0

    def add_items(self, count: int = 1) -> None:
        if count < 0:
            raise ValueError("count cannot be negative")
        self._items += count
        if self._items > self.limit.max_items:
            raise RuntimeError("test resource item limit exceeded")
        self.check_time()

    def check_time(self) -> None:
        elapsed_ms = (monotonic() - self._started) * 1000
        if elapsed_ms > self.limit.max_duration_ms:
            raise TimeoutError("test resource time limit exceeded")
