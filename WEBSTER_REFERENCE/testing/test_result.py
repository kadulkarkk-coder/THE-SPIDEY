"""Lightweight test result contracts for WEBSTER's validation layer."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TestResult:
    """Normalized result for one deterministic test case."""

    name: str
    passed: bool
    message: str = ""
    duration_ms: float = 0.0
    tags: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class TestSummary:
    """Aggregate outcome without retaining large test artifacts."""

    total: int
    passed: int
    failed: int

    @property
    def success_rate(self) -> float:
        return self.passed / self.total if self.total else 1.0
