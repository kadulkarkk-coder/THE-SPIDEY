"""Observable records for vision operations."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class VisionObservation:
    operation: str
    modality: str
    success: bool
    detail: str = ""
    timestamp: datetime | None = None


class VisionObserver:
    def __init__(self, max_events: int = 200) -> None:
        self.max_events = max(1, max_events)
        self._events: list[VisionObservation] = []

    def record(self, operation: str, modality: str, success: bool, detail: str = "") -> VisionObservation:
        item = VisionObservation(operation.strip(), modality.strip().lower(), bool(success), detail.strip(), datetime.now(timezone.utc))
        self._events.append(item)
        del self._events[:-self.max_events]
        return item

    def recent(self, limit: int = 20) -> tuple[VisionObservation, ...]:
        return tuple(self._events[-max(1, limit):])
