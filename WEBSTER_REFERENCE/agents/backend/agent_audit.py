"""Audit trail for agent assignments and outcomes."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class AgentAuditEntry:
    agent: str
    capability: str
    success: bool
    timestamp: datetime

class AgentAudit:
    def __init__(self): self._entries: list[AgentAuditEntry] = []
    def record(self, agent: str, capability: str, success: bool) -> AgentAuditEntry:
        entry = AgentAuditEntry(agent, capability, success, datetime.now(timezone.utc)); self._entries.append(entry); return entry
    def recent(self, limit: int = 20) -> tuple[AgentAuditEntry, ...]: return tuple(self._entries[-max(1, limit):])
