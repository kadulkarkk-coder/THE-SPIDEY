"""Controlled execution boundary for agents."""
from __future__ import annotations
from .base_agent import AgentRequest, AgentResult, BaseAgent

class AgentExecutor:
    def execute(self, agent: BaseAgent, request: AgentRequest) -> AgentResult:
        try:
            return agent.execute(request)
        except Exception as exc:
            return AgentResult(False, error=f"{exc.__class__.__name__}: {exc}")
