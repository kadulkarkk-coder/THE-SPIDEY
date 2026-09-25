"""Consolidate duplicate memory records into a compact view."""
from __future__ import annotations
from .memory_store import MemoryRecord

class MemoryConsolidator:
    def consolidate(self, records: tuple[MemoryRecord, ...]) -> tuple[MemoryRecord, ...]:
        seen: set[tuple[str, str]] = set()
        result: list[MemoryRecord] = []
        for record in records:
            signature = (record.key.lower(), str(record.value).strip().lower())
            if signature not in seen:
                seen.add(signature)
                result.append(record)
        return tuple(result)
