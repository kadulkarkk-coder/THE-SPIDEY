"""Goal decomposition into small, inspectable reasoning units."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Decomposition:
    goal: str
    units: tuple[str, ...]


class DecompositionEngine:
    """Splits explicit multi-part goals without pretending to solve them."""

    SEPARATORS = (" then ", " and then ", ";", " -> ")

    def decompose(self, goal: str) -> Decomposition:
        cleaned = " ".join(goal.split())
        if not cleaned:
            return Decomposition("", ())
        units = [cleaned]
        for separator in self.SEPARATORS:
            expanded = []
            for unit in units:
                expanded.extend(part.strip() for part in unit.split(separator) if part.strip())
            units = expanded
        return Decomposition(cleaned, tuple(units))
