"""Small offline-first queue for cross-device WEBSTER changes."""
from __future__ import annotations

from threading import RLock

from .sync_types import SyncRecord, SyncStatus


class SyncQueue:
    """Bounded, thread-safe queue that never requires network access."""

    def __init__(self, max_items: int = 1000) -> None:
        if max_items < 1:
            raise ValueError("max_items must be positive")
        self._max_items = max_items
        self._items: list[SyncRecord] = []
        self._lock = RLock()

    def enqueue(self, record: SyncRecord) -> SyncRecord:
        with self._lock:
            queued = SyncRecord(record.record_id, record.kind, record.payload, record.device_id, record.timestamp, SyncStatus.QUEUED)
            self._items.append(queued)
            if len(self._items) > self._max_items:
                del self._items[: len(self._items) - self._max_items]
            return queued

    def pending(self) -> tuple[SyncRecord, ...]:
        with self._lock:
            return tuple(self._items)

    def mark_synced(self, record_id: str) -> None:
        with self._lock:
            self._items = [
                SyncRecord(item.record_id, item.kind, item.payload, item.device_id, item.timestamp, SyncStatus.SYNCED)
                if item.record_id == record_id else item
                for item in self._items
            ]

    def clear_synced(self) -> None:
        with self._lock:
            self._items = [item for item in self._items if item.status != SyncStatus.SYNCED]
