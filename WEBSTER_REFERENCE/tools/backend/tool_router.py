"""Select tools using explicit capability metadata and risk preference."""
from __future__ import annotations
from .tool_registry import ToolRegistry
from .tool_contract import ToolBinding

class ToolRouter:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def route(self, capability: str, *, max_risk: str = "high") -> ToolBinding | None:
        order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        ceiling = order.get(max_risk.lower(), 2)
        for name in self.registry.names():
            binding = self.registry.get(name)
            if binding and capability.strip().lower() in {x.lower() for x in binding.spec.capabilities}:
                if order.get(binding.spec.risk.lower(), 3) <= ceiling:
                    return binding
        return None
