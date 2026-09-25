"""Small deterministic benchmark harness for intelligence components."""
from __future__ import annotations
from dataclasses import dataclass
from time import perf_counter

@dataclass(frozen=True)
class BenchmarkResult:
    name: str
    elapsed_seconds: float
    passed: bool

class BenchmarkRunner:
    def run(self, name: str, operation) -> BenchmarkResult:
        started = perf_counter()
        try:
            operation()
            passed = True
        except Exception:
            passed = False
        return BenchmarkResult(name, perf_counter() - started, passed)
