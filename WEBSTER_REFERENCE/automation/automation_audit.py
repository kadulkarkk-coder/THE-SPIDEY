"""Compact audit trail for automation lifecycle events."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class AutomationAuditEntry:
    task_id: str
    event: str
    detail: str = ""
    timestamp: datetime = None

class AutomationAudit:
    def __init__(self) -> None: self._entries: list[AutomationAuditEntry] = []
    def record(self, task_id: str, event: str, detail: str = "") -> AutomationAuditEntry:
        item = AutomationAuditEntry(task_id.strip(), event.strip().lower(), detail, datetime.now(timezone.utc))
        self._entries.append(item)
        return item
    def recent(self, limit: int = 20) -> tuple[AutomationAuditEntry, ...]: return tuple(self._entries[-max(1, limit):])
