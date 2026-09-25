"""Consistency checks for structured WEBSTER results."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ConsistencyResult:
    consistent: bool
    issues: tuple[str, ...] = ()

class ConsistencyChecker:
    def check(self, claims: list[str] | tuple[str, ...]) -> ConsistencyResult:
        normalized = [" ".join(str(c).lower().split()) for c in claims if str(c).strip()]
        issues: list[str] = []
        seen: set[str] = set()
        for claim in normalized:
            if claim in seen:
                issues.append(f"duplicate claim: {claim}")
            seen.add(claim)
        return ConsistencyResult(not issues, tuple(issues))
