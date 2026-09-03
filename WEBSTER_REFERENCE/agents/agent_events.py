"""Agent lifecycle events for observability."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class AgentEvent:
    agent: str
    event: str
    task: str
    timestamp: datetime

class AgentEventLog:
    def __init__(self): self._events: list[AgentEvent] = []
    def emit(self, agent: str, event: str, task: str) -> AgentEvent:
        item = AgentEvent(agent.strip(), event.strip(), task.strip(), datetime.now(timezone.utc)); self._events.append(item); return item
    def recent(self, limit: int = 20) -> tuple[AgentEvent, ...]: return tuple(self._events[-max(1, limit):])
