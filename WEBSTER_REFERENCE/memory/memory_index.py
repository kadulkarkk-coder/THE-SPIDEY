"""In-memory index for fast key/kind lookup."""
from __future__ import annotations
from collections import defaultdict

class MemoryIndex:
    def __init__(self) -> None:
        self._keys: dict[str, set[str]] = defaultdict(set)
        self._kinds: dict[str, set[str]] = defaultdict(set)

    def add(self, record_id: str, key: str, kind: str) -> None:
        self._keys[key.strip().lower()].add(record_id)
        self._kinds[kind.strip().lower()].add(record_id)

    def by_key(self, key: str) -> tuple[str, ...]:
        return tuple(sorted(self._keys.get(key.strip().lower(), ())))

    def by_kind(self, kind: str) -> tuple[str, ...]:
        return tuple(sorted(self._kinds.get(kind.strip().lower(), ())))

    def remove(self, record_id: str) -> None:
        for bucket in (*self._keys.values(), *self._kinds.values()):
            bucket.discard(record_id)
