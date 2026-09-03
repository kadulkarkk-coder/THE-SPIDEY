"""Dependency-free layered memory store for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import RLock
from uuid import uuid4
from typing import Any


@dataclass(frozen=True)
class MemoryRecord:
    key: str
    value: Any
    kind: str = "general"
    id: str = field(default_factory=lambda: uuid4().hex)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: tuple[tuple[str, str], ...] = ()


class MemoryStore:
    """Thread-safe in-process store; persistence adapters can be added later."""

    def __init__(self) -> None:
        self._records: dict[str, MemoryRecord] = {}
        self._lock = RLock()

    def put(self, key: str, value: Any, *, kind: str = "general", metadata: dict[str, str] | None = None) -> MemoryRecord:
        key = key.strip()
        if not key:
            raise ValueError("Memory key cannot be empty")
        record = MemoryRecord(key, value, kind.strip() or "general", metadata=tuple(sorted((metadata or {}).items())))
        with self._lock:
            self._records[record.id] = record
        return record

    def get(self, record_id: str) -> MemoryRecord | None:
        with self._lock:
            return self._records.get(record_id)

    def all(self, *, kind: str | None = None) -> tuple[MemoryRecord, ...]:
        with self._lock:
            values = tuple(self._records.values())
        if kind is None:
            return values
        return tuple(record for record in values if record.kind == kind)

    def delete(self, record_id: str) -> bool:
        with self._lock:
            return self._records.pop(record_id, None) is not None

    def count(self) -> int:
        with self._lock:
            return len(self._records)
