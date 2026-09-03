"""Event-oriented episodic memory for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .memory_store import MemoryRecord, MemoryStore


@dataclass(frozen=True)
class Episode:
    event: str
    outcome: str = ""
    context: str = ""
    timestamp: datetime = datetime.min


class EpisodicMemory:
    """Stores interaction episodes separately from durable preferences."""

    KIND = "episodic"

    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def remember(self, event: str, *, outcome: str = "", context: str = "") -> MemoryRecord:
        event = " ".join(event.split())
        if not event:
            raise ValueError("Episode event cannot be empty")
        episode = Episode(event, outcome.strip(), context.strip(), datetime.now(timezone.utc))
        return self.store.put(event, episode, kind=self.KIND)

    def recent(self, limit: int = 10) -> tuple[MemoryRecord, ...]:
        records = self.store.all(kind=self.KIND)
        return tuple(sorted(records, key=lambda item: item.created_at, reverse=True)[:max(0, limit)])
