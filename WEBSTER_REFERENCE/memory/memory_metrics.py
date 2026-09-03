"""Observable metrics for the memory layer."""
from __future__ import annotations
from dataclasses import dataclass
from .memory_store import MemoryStore

@dataclass(frozen=True)
class MemoryMetrics:
    total: int
    general: int
    episodic: int
    preferences: int

class MemoryMetricsCollector:
    def collect(self, store: MemoryStore) -> MemoryMetrics:
        records = store.all()
        counts = {kind: sum(r.kind == kind for r in records) for kind in ("general", "episodic", "preference")}
        return MemoryMetrics(len(records), counts["general"], counts["episodic"], counts["preference"])
