"""Small dependency-free test runner for WEBSTER reference modules."""
from __future__ import annotations

from time import monotonic
from typing import Callable, Iterable

from .test_result import TestResult, TestSummary


class TestRunner:
    """Run supplied test callables without background workers or persistent state."""

    def run(self, tests: Iterable[tuple[str, Callable[[], None]]]) -> tuple[tuple[TestResult, ...], TestSummary]:
        results: list[TestResult] = []
        for name, test in tests:
            started = monotonic()
            try:
                test()
            except Exception as exc:
                results.append(TestResult(name, False, str(exc), (monotonic() - started) * 1000))
            else:
                results.append(TestResult(name, True, "ok", (monotonic() - started) * 1000))
        passed = sum(item.passed for item in results)
        summary = TestSummary(len(results), passed, len(results) - passed)
        return tuple(results), summary
