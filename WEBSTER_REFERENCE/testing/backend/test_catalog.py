"""Named test catalog for deterministic WEBSTER validation suites."""
from __future__ import annotations

from threading import RLock
from typing import Callable


class TestCatalog:
    """Register named tests by suite while preventing duplicate names."""

    def __init__(self) -> None:
        self._tests: dict[str, dict[str, Callable[[], None]]] = {}
        self._lock = RLock()

    def register(self, suite: str, name: str, test: Callable[[], None]) -> None:
        suite = suite.strip()
        name = name.strip()
        if not suite or not name:
            raise ValueError("suite and test name are required")
        with self._lock:
            bucket = self._tests.setdefault(suite, {})
            if name in bucket:
                raise ValueError(f"test already registered: {suite}/{name}")
            bucket[name] = test

    def suite(self, suite: str) -> tuple[tuple[str, Callable[[], None]], ...]:
        with self._lock:
            return tuple(self._tests.get(suite, {}).items())

    def suites(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(self._tests)
