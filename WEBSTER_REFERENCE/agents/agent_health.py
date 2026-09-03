"""Basic health and availability tracking for agents."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class AgentHealth:
    available: bool = True
    failures: int = 0
    last_error: str | None = None

class AgentHealthTracker:
    def __init__(self): self._health: dict[str, AgentHealth] = {}
    def record_success(self, name: str) -> None: self._health[name] = AgentHealth(True, self._health.get(name, AgentHealth()).failures)
    def record_failure(self, name: str, error: str) -> None:
        old = self._health.get(name, AgentHealth()); self._health[name] = AgentHealth(False, old.failures + 1, error)
    def get(self, name: str) -> AgentHealth: return self._health.get(name, AgentHealth())
