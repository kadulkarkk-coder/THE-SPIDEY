"""Observable records for desktop operations."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class DesktopObservation:
    operation: str
    principal: str
    success: bool
    detail: str = ""
    timestamp: datetime | None = None

class DesktopObserver:
    def __init__(self) -> None:
        self._items: list[DesktopObservation] = []

    def record(self, operation: str, principal: str, success: bool, detail: str = "") -> DesktopObservation:
        item = DesktopObservation(operation.strip(), principal.strip(), bool(success), detail, datetime.now(timezone.utc))
        self._items.append(item)
        return item

    def recent(self, limit: int = 20) -> tuple[DesktopObservation, ...]:
        return tuple(self._items[-max(1, limit):])
