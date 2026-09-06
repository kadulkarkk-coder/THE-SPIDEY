"""Benchmark gate for comparing an evolved plugin with its parent."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkResult:
    baseline: float
    candidate: float
    improvement: float
    accepted: bool


class EvolutionBenchmark:
    """Accept candidates only when they meet a measurable improvement gate."""

    def compare(self, baseline: float, candidate: float, *, minimum_improvement: float = 0.01) -> BenchmarkResult:
        if not 0.0 <= baseline <= 1.0 or not 0.0 <= candidate <= 1.0:
            raise ValueError("benchmark scores must be between 0 and 1")
        if minimum_improvement < 0:
            raise ValueError("minimum_improvement must not be negative")
        improvement = candidate - baseline
        return BenchmarkResult(baseline, candidate, improvement, improvement >= minimum_improvement)
