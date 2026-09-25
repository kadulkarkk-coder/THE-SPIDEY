"""User-authorized memory deletion boundary."""
from __future__ import annotations
from .memory_store import MemoryStore

class MemoryDeleter:
    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def delete(self, record_id: str, *, authorized: bool = False) -> bool:
        if not authorized:
            raise PermissionError("memory deletion requires explicit authorization")
        return self.store.delete(record_id)
