"""Retain recent agent results for coordination and inspection."""
from __future__ import annotations
from .base_agent import AgentResult

class AgentResultStore:
    def __init__(self, max_results: int = 100): self.max_results = max(1, max_results); self._results: list[AgentResult] = []
    def add(self, result: AgentResult) -> None:
        self._results.append(result); del self._results[:-self.max_results]
    def recent(self, limit: int = 20) -> tuple[AgentResult, ...]: return tuple(self._results[-max(1, limit):])
