"""Regression-suite contracts for protecting previously working behavior."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class RegressionCase:
    name: str
    check: Callable[[], None]
    baseline: str = ""


class RegressionSuite:
    def __init__(self) -> None:
        self._cases: list[RegressionCase] = []

    def add(self, case: RegressionCase) -> None:
        if not case.name.strip():
            raise ValueError("regression case name is required")
        if not callable(case.check):
            raise TypeError("regression check must be callable")
        if any(existing.name == case.name for existing in self._cases):
            raise ValueError(f"duplicate regression case: {case.name}")
        self._cases.append(case)

    def cases(self) -> tuple[RegressionCase, ...]:
        return tuple(self._cases)

    def run(self) -> tuple[str, ...]:
        failures: list[str] = []
        for case in self._cases:
            try:
                case.check()
            except Exception as exc:
                failures.append(f"{case.name}: {exc}")
        return tuple(failures)
