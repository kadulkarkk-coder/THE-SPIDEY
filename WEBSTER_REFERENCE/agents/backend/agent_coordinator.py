"""Coordinate sequential agent execution with explicit hand-offs."""
from __future__ import annotations
from .base_agent import AgentRequest, AgentResult, BaseAgent
from .agent_executor import AgentExecutor

class AgentCoordinator:
    def __init__(self, executor: AgentExecutor | None = None): self.executor = executor or AgentExecutor()
    def run(self, agents: tuple[BaseAgent, ...], task: str) -> tuple[AgentResult, ...]:
        results = []
        context = {}
        for agent in agents:
            result = self.executor.execute(agent, AgentRequest(task, context.copy()))
            results.append(result)
            if not result.success: break
            context[agent.name] = result.output
        return tuple(results)
