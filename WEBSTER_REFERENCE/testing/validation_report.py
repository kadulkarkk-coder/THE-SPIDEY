"""Aggregated validation reporting for WEBSTER test phases."""
from __future__ import annotations

from dataclasses import dataclass
from .test_result import TestResult


@dataclass(frozen=True)
class ValidationReport:
    phase: str
    results: tuple[TestResult, ...]

    @property
    def passed(self) -> int:
        return sum(result.passed for result in self.results)

    @property
    def failed(self) -> int:
        return len(self.results) - self.passed

    @property
    def success_rate(self) -> float:
        return self.passed / len(self.results) if self.results else 1.0

    @property
    def healthy(self) -> bool:
        return self.failed == 0
