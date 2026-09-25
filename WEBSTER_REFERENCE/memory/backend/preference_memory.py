"""Explicit, user-controlled preference memory for WEBSTER."""
from __future__ import annotations

from .memory_store import MemoryRecord, MemoryStore


class PreferenceMemory:
    """Stores named preferences with explicit overwrite and removal operations."""

    KIND = "preference"

    def __init__(self, store: MemoryStore) -> None:
        self.store = store
        self._keys: dict[str, str] = {}

    def set(self, name: str, value: str) -> MemoryRecord:
        name = name.strip()
        if not name:
            raise ValueError("Preference name cannot be empty")
        old_id = self._keys.get(name)
        if old_id:
            self.store.delete(old_id)
        record = self.store.put(name, value, kind=self.KIND)
        self._keys[name] = record.id
        return record

    def get(self, name: str, default: str | None = None) -> str | None:
        record_id = self._keys.get(name.strip())
        record = self.store.get(record_id) if record_id else None
        return str(record.value) if record else default

    def remove(self, name: str) -> bool:
        key = name.strip()
        record_id = self._keys.pop(key, None)
        return self.store.delete(record_id) if record_id else False

    def all(self) -> dict[str, str]:
        return {key: str(self.get(key, "")) for key in tuple(self._keys)}
