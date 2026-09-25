"""Short-lived contextual memory assembled for a request."""
from __future__ import annotations
from dataclasses import dataclass
from .memory_store import MemoryRecord

@dataclass(frozen=True)
class ContextMemory:
    records: tuple[MemoryRecord, ...]

    def keys(self) -> tuple[str, ...]:
        return tuple(record.key for record in self.records)

class ContextMemoryBuilder:
    def build(self, records: tuple[MemoryRecord, ...], *, limit: int = 8) -> ContextMemory:
        return ContextMemory(records[-max(1, limit):])
