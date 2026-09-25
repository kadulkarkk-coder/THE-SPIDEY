"""Lifecycle operations for memory records."""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from .memory_store import MemoryStore

class MemoryLifecycle:
    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def purge_before(self, cutoff: datetime) -> int:
        removed = 0
        for record in self.store.all():
            if record.created_at < cutoff and self.store.delete(record.id):
                removed += 1
        return removed

    def purge_older_than(self, seconds: int) -> int:
        if seconds < 0: raise ValueError("seconds must be non-negative")
        return self.purge_before(datetime.now(timezone.utc) - timedelta(seconds=seconds))
