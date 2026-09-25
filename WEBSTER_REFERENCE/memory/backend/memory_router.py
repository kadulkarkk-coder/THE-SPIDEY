"""Route memory operations to specialized memory components."""
from __future__ import annotations
from .memory_store import MemoryStore
from .memory_retriever import MemoryRetriever

class MemoryRouter:
    def __init__(self, store: MemoryStore | None = None) -> None:
        self.store = store or MemoryStore()
        self.retriever = MemoryRetriever(self.store)

    def remember(self, key: str, value: object, *, kind: str = "general"):
        return self.store.put(key, value, kind=kind)

    def recall(self, query: str, *, limit: int = 5):
        return self.retriever.search(query, limit=limit)
