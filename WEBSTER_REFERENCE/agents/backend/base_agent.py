"""Shared agent contract and controlled lifecycle boundary."""
from __future__ import annotations
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Any

@dataclass(frozen=True)
class AgentRequest:
    task: str
    context: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class AgentResult:
    success: bool
    output: Any = None
    error: str | None = None

class BaseAgent(ABC):
    name = "agent"
    capabilities: frozenset[str] = frozenset()

    @abstractmethod
    def execute(self, request: AgentRequest) -> AgentResult:
        raise NotImplementedError

    def can_handle(self, capability: str) -> bool:
        return capability in self.capabilities
