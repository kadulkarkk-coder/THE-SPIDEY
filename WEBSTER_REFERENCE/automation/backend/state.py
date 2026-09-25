"""Observable lifecycle state for automation workflows."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class AutomationState:
    task_id: str
    status: str
    updated_at: datetime
    error: str | None = None

class AutomationStateStore:
    VALID = frozenset({"queued", "running", "completed", "failed", "cancelled"})
    def __init__(self) -> None: self._states: dict[str, AutomationState] = {}
    def set(self, task_id: str, status: str, error: str | None = None) -> AutomationState:
        status = status.strip().lower()
        if status not in self.VALID: raise ValueError(f"invalid automation status: {status}")
        item = AutomationState(task_id.strip(), status, datetime.now(timezone.utc), error)
        self._states[item.task_id] = item
        return item
    def get(self, task_id: str) -> AutomationState | None: return self._states.get(task_id.strip())
