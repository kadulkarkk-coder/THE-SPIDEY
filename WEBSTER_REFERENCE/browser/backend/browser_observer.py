"""Observable records for browser operations."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class BrowserObservation:
    operation: str
    target: str
    success: bool
    detail: str = ""
    timestamp: datetime = None

class BrowserObserver:
    def __init__(self) -> None: self._items: list[BrowserObservation] = []
    def record(self, operation: str, target: str, success: bool, detail: str = "") -> BrowserObservation:
        item = BrowserObservation(operation.strip(), target.strip(), bool(success), detail, datetime.now(timezone.utc)); self._items.append(item); return item
    def recent(self, limit: int = 20) -> tuple[BrowserObservation, ...]: return tuple(self._items[-max(1, limit):])
