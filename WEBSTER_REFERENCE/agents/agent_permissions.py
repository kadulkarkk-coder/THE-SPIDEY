"""Permission boundary for agent capabilities."""
from __future__ import annotations

class AgentPermissionPolicy:
    def __init__(self): self._allowed: dict[str, set[str]] = {}
    def allow(self, agent: str, capability: str) -> None: self._allowed.setdefault(agent.strip().lower(), set()).add(capability.strip().lower())
    def permitted(self, agent: str, capability: str) -> bool: return capability.strip().lower() in self._allowed.get(agent.strip().lower(), set())
