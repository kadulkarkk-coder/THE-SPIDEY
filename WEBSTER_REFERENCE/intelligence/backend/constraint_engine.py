"""Explicit constraint evaluation for WEBSTER intelligence decisions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Constraint:
    name: str
    check: Callable[[str], bool]
    description: str = ""


@dataclass(frozen=True)
class ConstraintResult:
    allowed: bool
    failed: tuple[str, ...] = ()


class ConstraintEngine:
    """Evaluates explicit, inspectable constraints before execution."""

    def evaluate(self, text: str, constraints: list[Constraint]) -> ConstraintResult:
        failed = tuple(c.name for c in constraints if not c.check(text))
        return ConstraintResult(allowed=not failed, failed=failed)
