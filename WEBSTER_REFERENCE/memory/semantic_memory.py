"""Dependency-free semantic-ish memory matching using token overlap."""
from __future__ import annotations
from .memory_store import MemoryRecord

class SemanticMemory:
    @staticmethod
    def _tokens(text: str) -> set[str]:
        return {token.lower() for token in text.split() if token.strip()}

    def similarity(self, query: str, record: MemoryRecord) -> float:
        left, right = self._tokens(query), self._tokens(record.key + " " + str(record.value))
        if not left or not right:
            return 0.0
        return round(len(left & right) / len(left | right), 4)

    def rank(self, query: str, records: list[MemoryRecord] | tuple[MemoryRecord, ...]) -> tuple[MemoryRecord, ...]:
        return tuple(sorted(records, key=lambda r: (-self.similarity(query, r), r.created_at)))
