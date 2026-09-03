"""Duplicate detection for WEBSTER memory records."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .memory_store import MemoryRecord


@dataclass(frozen=True)
class DuplicateMatch:
    existing: MemoryRecord
    fingerprint: str


class MemoryDeduplicator:
    """Uses normalized key/value fingerprints to detect exact duplicates."""

    @staticmethod
    def fingerprint(record: MemoryRecord) -> str:
        normalized = f"{record.kind}|{record.key.strip().lower()}|{str(record.value).strip().lower()}"
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    def find(self, candidate: MemoryRecord, existing: tuple[MemoryRecord, ...]) -> DuplicateMatch | None:
        target = self.fingerprint(candidate)
        for record in existing:
            if record.id != candidate.id and self.fingerprint(record) == target:
                return DuplicateMatch(record, target)
        return None

    def unique(self, records: tuple[MemoryRecord, ...]) -> tuple[MemoryRecord, ...]:
        seen: set[str] = set()
        result: list[MemoryRecord] = []
        for record in records:
            fingerprint = self.fingerprint(record)
            if fingerprint not in seen:
                seen.add(fingerprint)
                result.append(record)
        return tuple(result)
