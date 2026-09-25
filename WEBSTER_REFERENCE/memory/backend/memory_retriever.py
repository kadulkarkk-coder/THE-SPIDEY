"""Relevant-memory retrieval for WEBSTER using transparent lexical scoring."""
from __future__ import annotations

import re
from dataclasses import dataclass

from .memory_store import MemoryRecord, MemoryStore


@dataclass(frozen=True)
class Retrieval:
    record: MemoryRecord
    score: float


class MemoryRetriever:
    """Retrieves records by token overlap without requiring embeddings or APIs."""

    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return {token for token in re.findall(r"[a-zA-Z0-9_]+", text.lower()) if len(token) > 1}

    def search(self, query: str, *, limit: int = 5, kind: str | None = None) -> tuple[Retrieval, ...]:
        if limit < 1:
            return ()
        query_tokens = self._tokens(query)
        if not query_tokens:
            return ()
        matches: list[Retrieval] = []
        for record in self.store.all(kind=kind):
            haystack = self._tokens(f"{record.key} {record.value}")
            overlap = len(query_tokens & haystack)
            if overlap:
                matches.append(Retrieval(record, overlap / len(query_tokens)))
        matches.sort(key=lambda item: item.score, reverse=True)
        return tuple(matches[:limit])
