"""Explicit approval boundary for sensitive automation actions."""
from __future__ import annotations

class ApprovalGate:
    def __init__(self) -> None: self._approved: set[str] = set()
    def approve(self, task_id: str) -> None: self._approved.add(task_id.strip())
    def revoke(self, task_id: str) -> None: self._approved.discard(task_id.strip())
    def allowed(self, task_id: str, *, required: bool = True) -> bool:
        return (not required) or task_id.strip() in self._approved
