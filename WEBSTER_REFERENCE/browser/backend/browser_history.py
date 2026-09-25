"""Bounded browser navigation history."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class HistoryEntry:
    url: str
    title: str | None = None
    visited_at: datetime = None

class BrowserHistory:
    def __init__(self, max_entries: int = 100) -> None: self.max_entries = max(1, max_entries); self._entries: list[HistoryEntry] = []
    def add(self, url: str, title: str | None = None) -> HistoryEntry:
        item = HistoryEntry(url.strip(), title, datetime.now(timezone.utc)); self._entries.append(item); del self._entries[:-self.max_entries]; return item
    def recent(self, limit: int = 20) -> tuple[HistoryEntry, ...]: return tuple(reversed(self._entries[-max(1, limit):]))
    def clear(self) -> None: self._entries.clear()
