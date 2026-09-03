"""Expiration helpers for time-limited memory."""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from .memory_store import MemoryStore

class MemoryExpiry:
    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def expired(self, created_at: datetime, ttl_seconds: int) -> bool:
        if ttl_seconds < 0:
            raise ValueError("ttl_seconds must be non-negative")
        return datetime.now(timezone.utc) >= created_at + timedelta(seconds=ttl_seconds)

    def purge(self, ttl_seconds: int, *, kind: str | None = None) -> int:
        removed = 0
        for record in self.store.all(kind=kind):
            if self.expired(record.created_at, ttl_seconds) and self.store.delete(record.id):
                removed += 1
        return removed
