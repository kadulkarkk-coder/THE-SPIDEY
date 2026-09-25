"""Portable notification event bridge; UI-specific delivery stays optional."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class Notification:
    title: str
    message: str
    level: str
    created_at: datetime

class NotificationBridge:
    LEVELS = frozenset({"info", "success", "warning", "error"})
    def __init__(self) -> None: self._items: list[Notification] = []
    def notify(self, title: str, message: str, level: str = "info") -> Notification:
        title, message, level = title.strip(), message.strip(), level.strip().lower()
        if not title or not message: raise ValueError("title and message are required")
        if level not in self.LEVELS: raise ValueError("invalid notification level")
        item = Notification(title, message, level, datetime.now(timezone.utc)); self._items.append(item); return item
    def recent(self, limit: int = 20) -> tuple[Notification, ...]: return tuple(self._items[-max(1, limit):])
