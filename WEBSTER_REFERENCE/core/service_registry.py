"""Runtime service registry for WEBSTER."""
from __future__ import annotations
from typing import Any
from .component_registry import ComponentRegistry, ComponentRecord

class ServiceRegistry(ComponentRegistry):
    """Named service capabilities with explicit registration and resolution."""
    def register_service(self, name: str, service: Any, description: str = "") -> ComponentRecord:
        return self.register(name, service, description)

    def resolve(self, name: str) -> Any | None:
        return self.get(name)
