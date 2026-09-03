"""Observable lifecycle state for an agent."""
from __future__ import annotations
from dataclasses import dataclass
from threading import RLock

@dataclass(frozen=True)
class AgentState:
    status: str = "idle"
    task_count: int = 0
    last_error: str | None = None

class AgentStateStore:
    def __init__(self) -> None:
        self._states: dict[str, AgentState] = {}; self._lock = RLock()
    def set(self, name: str, state: AgentState) -> None:
        with self._lock: self._states[name.strip().lower()] = state
    def get(self, name: str) -> AgentState:
        with self._lock: return self._states.get(name.strip().lower(), AgentState())
