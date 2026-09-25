"""Lineage and rollback records for WEBSTER's plugin-based evolution."""
from __future__ import annotations

from dataclasses import dataclass
from time import time


@dataclass(frozen=True)
class EvolutionRecord:
    evolution_id: str
    plugin_id: str
    version: str
    parent_version: str
    status: str
    rollback_version: str = ""
    timestamp: float = time()


class EvolutionLineage:
    """Bounded append-only lineage history for reversible evolution."""

    def __init__(self, max_records: int = 200) -> None:
        if max_records < 1:
            raise ValueError("max_records must be positive")
        self._max_records = max_records
        self._records: list[EvolutionRecord] = []

    def record(self, item: EvolutionRecord) -> None:
        self._records.append(item)
        if len(self._records) > self._max_records:
            del self._records[: len(self._records) - self._max_records]

    def records(self) -> tuple[EvolutionRecord, ...]:
        return tuple(self._records)

    def latest(self, plugin_id: str) -> EvolutionRecord | None:
        for item in reversed(self._records):
            if item.plugin_id == plugin_id:
                return item
        return None
