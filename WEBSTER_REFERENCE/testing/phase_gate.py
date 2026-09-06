"""Simple pass/fail gate used before advancing WEBSTER phases."""
from __future__ import annotations

from dataclasses import dataclass
from .validation_report import ValidationReport


@dataclass(frozen=True)
class PhaseGate:
    required_success_rate: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.required_success_rate <= 1.0:
            raise ValueError("required_success_rate must be between 0 and 1")

    def evaluate(self, report: ValidationReport) -> bool:
        return report.success_rate >= self.required_success_rate and report.healthy
