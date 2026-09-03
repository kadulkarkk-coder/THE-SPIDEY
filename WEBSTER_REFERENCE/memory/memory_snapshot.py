"""Serializable point-in-time view of the memory layer."""
from __future__ import annotations
from dataclasses import dataclass
from .memory_store import MemoryStore, MemoryRecord

@dataclass(frozen=True)
class MemorySnapshot:
    records: tuple[MemoryRecord, ...]

class MemorySnapshotter:
    def capture(self, store: MemoryStore) -> MemorySnapshot:
        return MemorySnapshot(store.all())

    def restore(self, store: MemoryStore, snapshot: MemorySnapshot) -> int:
        restored = 0
        for record in snapshot.records:
            if store.get(record.id) is None:
                store._records[record.id] = record
                restored += 1
        return restored
