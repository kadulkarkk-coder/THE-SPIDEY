"""Manifest and lifecycle metadata for evolved WEBSTER plugins."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class EvolutionPluginManifest:
    evolution_id: str
    plugin_id: str
    version: str
    parent_version: str
    problem_solved: str
    expected_improvement: str
    tests: tuple[str, ...] = ()
    benchmark_score: float | None = None
    permissions: tuple[str, ...] = ()
    resource_limits: Mapping[str, str] = field(default_factory=dict)
    dependencies: tuple[str, ...] = ()
    rollback_version: str = ""

    def __post_init__(self) -> None:
        if not self.evolution_id.strip() or not self.plugin_id.strip() or not self.version.strip():
            raise ValueError("evolution_id, plugin_id, and version are required")
        if self.benchmark_score is not None and not 0.0 <= self.benchmark_score <= 1.0:
            raise ValueError("benchmark_score must be between 0 and 1")
