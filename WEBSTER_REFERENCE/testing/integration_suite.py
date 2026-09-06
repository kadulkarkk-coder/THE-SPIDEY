"""Lightweight integration-suite helpers for WEBSTER subsystem contracts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .test_result import TestResult, TestSummary
from .test_runner import TestRunner


@dataclass(frozen=True)
class IntegrationReport:
    """Result of one named integration suite."""

    suite: str
    results: tuple[TestResult, ...]
    summary: TestSummary


class IntegrationSuite:
    """Group integration checks and execute them deterministically."""

    def __init__(self, suite: str, *, runner: TestRunner | None = None) -> None:
        suite = suite.strip()
        if not suite:
            raise ValueError("suite name is required")
        self.suite = suite
        self._tests: list[tuple[str, Callable[[], None]]] = []
        self._runner = runner or TestRunner()

    def add(self, name: str, test: Callable[[], None]) -> "IntegrationSuite":
        name = name.strip()
        if not name:
            raise ValueError("test name is required")
        if any(existing == name for existing, _ in self._tests):
            raise ValueError(f"test already registered: {self.suite}/{name}")
        self._tests.append((name, test))
        return self

    def run(self) -> IntegrationReport:
        results, summary = self._runner.run(tuple(self._tests))
        return IntegrationReport(self.suite, results, summary)

    def extend(self, tests: Iterable[tuple[str, Callable[[], None]]]) -> "IntegrationSuite":
        for name, test in tests:
            self.add(name, test)
        return self
