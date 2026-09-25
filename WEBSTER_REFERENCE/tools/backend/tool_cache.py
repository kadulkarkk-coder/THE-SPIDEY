"""Small in-process cache for deterministic, reusable tool results."""
from __future__ import annotations
from dataclasses import dataclass
from time import monotonic

@dataclass(frozen=True)
class CacheEntry:
    value: object
    expires_at: float | None = None

class ToolCache:
    def __init__(self) -> None:
        self._items: dict[str, CacheEntry] = {}

    def put(self, key: str, value: object, ttl_seconds: float | None = None) -> None:
        if not key.strip(): raise ValueError("cache key is required")
        if ttl_seconds is not None and ttl_seconds < 0: raise ValueError("ttl_seconds must be non-negative")
        expiry = None if ttl_seconds is None else monotonic() + ttl_seconds
        self._items[key.strip()] = CacheEntry(value, expiry)

    def get(self, key: str):
        item = self._items.get(key.strip())
        if item is None: return None
        if item.expires_at is not None and monotonic() >= item.expires_at:
            self._items.pop(key.strip(), None)
            return None
        return item.value

    def invalidate(self, key: str) -> bool:
        return self._items.pop(key.strip(), None) is not None

    def clear(self) -> None:
        self._items.clear()
