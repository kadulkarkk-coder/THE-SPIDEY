"""Select an agent by explicit capability."""
from __future__ import annotations
from .agent_registry import AgentRegistry

class AgentRouter:
    def __init__(self, registry: AgentRegistry) -> None: self.registry = registry
    def route(self, capability: str):
        for name in self.registry.names():
            agent = self.registry.get(name)
            if agent and agent.can_handle(capability): return agent
        return None
