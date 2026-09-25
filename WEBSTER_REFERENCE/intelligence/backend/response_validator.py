"""Validation boundary for intelligence responses."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    issues: tuple[str, ...] = ()

class ResponseValidator:
    def validate(self, text: str, *, confidence: float = 1.0) -> ValidationResult:
        issues: list[str] = []
        if not text or not text.strip():
            issues.append("empty response")
        if not 0.0 <= confidence <= 1.0:
            issues.append("confidence out of range")
        return ValidationResult(not issues, tuple(issues))
