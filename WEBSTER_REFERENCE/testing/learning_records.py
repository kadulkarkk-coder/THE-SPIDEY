"""Structured records used by WEBSTER's local learning loop."""
from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Mapping


@dataclass(frozen=True)
class LearningRecord:
    """A compact observation of a completed WEBSTER interaction."""

    event: str
    outcome: str
    score: float = 0.0
    metadata: Mapping[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time)


class LearningStore:
    """Bounded in-memory store; no raw prompts or sensitive payloads are required."""

    def __init__(self, max_records: int = 500) -> None:
        if max_records < 1:
            raise ValueError("max_records must be positive")
        self._max_records = max_records
        self._records: list[LearningRecord] = []

    def add(self, record: LearningRecord) -> None:
        self._records.append(record)
        if len(self._records) > self._max_records:
            del self._records[: len(self._records) - self._max_records]

    def records(self) -> tuple[LearningRecord, ...]:
        return tuple(self._records)
