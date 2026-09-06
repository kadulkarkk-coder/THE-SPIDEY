"""Safe candidate contracts for WEBSTER self-evolution."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class EvolutionCandidate:
    """Describes a proposed improvement without changing the running system."""

    evolution_id: str
    plugin_id: str
    version: str
    problem: str
    expected_improvement: str
    permissions: tuple[str, ...] = ()
    resource_limits: Mapping[str, str] = field(default_factory=dict)
    parent_version: str = ""

    def __post_init__(self) -> None:
        for value, label in ((self.evolution_id, "evolution_id"), (self.plugin_id, "plugin_id"),
                             (self.version, "version"), (self.problem, "problem")):
            if not value.strip():
                raise ValueError(f"{label} must not be empty")
        if any(not item.strip() for item in self.permissions):
            raise ValueError("permissions must not contain empty values")
