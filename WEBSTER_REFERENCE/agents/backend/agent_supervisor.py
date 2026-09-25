"""Supervisor enforcing health and permission checks before delegation."""
from __future__ import annotations
from .agent_router import AgentRouter
from .agent_permissions import AgentPermissionPolicy
from .agent_health import AgentHealthTracker
from .base_agent import AgentRequest, AgentResult

class AgentSupervisor:
    def __init__(self, router: AgentRouter, permissions: AgentPermissionPolicy | None = None, health: AgentHealthTracker | None = None):
        self.router = router; self.permissions = permissions or AgentPermissionPolicy(); self.health = health or AgentHealthTracker()
    def execute(self, capability: str, request: AgentRequest) -> AgentResult:
        agent = self.router.route(capability)
        if agent is None: return AgentResult(False, error=f"no agent supports capability: {capability}")
        if not self.permissions.permitted(agent.name, capability): return AgentResult(False, error="agent capability not permitted")
        if not self.health.get(agent.name).available: return AgentResult(False, error="agent is unavailable")
        return agent.execute(request)
