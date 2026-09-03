"""High-level coordinator for WEBSTER's memory and knowledge components."""
from __future__ import annotations
from .memory_store import MemoryStore
from .memory_router import MemoryRouter
from .memory_policy import MemoryPolicyEngine
from .memory_deleter import MemoryDeleter
from .memory_metrics import MemoryMetricsCollector

class MemoryManager:
    def __init__(self, store: MemoryStore | None = None) -> None:
        self.store = store or MemoryStore()
        self.router = MemoryRouter(self.store)
        self.policy = MemoryPolicyEngine()
        self.deleter = MemoryDeleter(self.store)
        self.metrics = MemoryMetricsCollector()

    def remember(self, key: str, value: object, *, kind: str = "general", sensitive: bool = False):
        policy = self.policy.decide(kind=kind, sensitive=sensitive)
        if not policy.retain:
            return None
        return self.router.remember(key, value, kind=kind)

    def recall(self, query: str, *, limit: int = 5):
        return self.router.recall(query, limit=limit)

    def stats(self):
        return self.metrics.collect(self.store)
