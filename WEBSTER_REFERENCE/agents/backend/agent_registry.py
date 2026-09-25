"""Registration and discovery of controlled agents."""
from __future__ import annotations
from threading import RLock
from .base_agent import BaseAgent

class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}
        self._lock = RLock()

    def register(self, agent: BaseAgent) -> None:
        name = agent.name.strip().lower()
        if not name: raise ValueError("agent name is required")
        with self._lock: self._agents[name] = agent

    def get(self, name: str) -> BaseAgent | None:
        with self._lock: return self._agents.get(name.strip().lower())

    def names(self) -> tuple[str, ...]:
        with self._lock: return tuple(sorted(self._agents))
