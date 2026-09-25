"""Deterministic local sync coordinator; transport remains replaceable."""
from __future__ import annotations

from threading import RLock
from typing import Callable

from .sync_queue import SyncQueue
from .sync_types import SyncRecord, SyncStatus


class SyncManager:
    """Coordinates local records and an optional authenticated transport."""

    def __init__(self, queue: SyncQueue | None = None) -> None:
        self.queue = queue or SyncQueue()
        self._transport: Callable[[SyncRecord], bool] | None = None
        self._lock = RLock()

    def set_transport(self, transport: Callable[[SyncRecord], bool] | None) -> None:
        with self._lock:
            self._transport = transport

    def submit(self, record: SyncRecord) -> SyncRecord:
        return self.queue.enqueue(record)

    def flush(self) -> int:
        """Send queued records when a caller supplies an authenticated transport."""
        with self._lock:
            transport = self._transport
        if transport is None:
            return 0
        synced = 0
        for record in self.queue.pending():
            if record.status != SyncStatus.QUEUED:
                continue
            if transport(record):
                self.queue.mark_synced(record.record_id)
                synced += 1
        return synced
