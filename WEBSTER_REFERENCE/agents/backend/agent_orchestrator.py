"""Top-level agent orchestration facade."""
from __future__ import annotations
from .agent_registry import AgentRegistry
from .agent_router import AgentRouter
from .agent_executor import AgentExecutor
from .base_agent import AgentRequest, AgentResult

class AgentOrchestrator:
    def __init__(self, registry: AgentRegistry | None = None):
        self.registry = registry or AgentRegistry(); self.router = AgentRouter(self.registry); self.executor = AgentExecutor()
    def run(self, capability: str, task: str, context: dict | None = None) -> AgentResult:
        agent = self.router.route(capability)
        if agent is None: return AgentResult(False, error=f"no agent for capability: {capability}")
        return self.executor.execute(agent, AgentRequest(task, context or {}))
