"""Capability metadata used by the agent router."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Capability:
    name: str
    description: str = ""
    risk: str = "low"

class CapabilityCatalog:
    def __init__(self): self._items: dict[str, Capability] = {}
    def add(self, capability: Capability) -> None: self._items[capability.name.strip().lower()] = capability
    def get(self, name: str) -> Capability | None: return self._items.get(name.strip().lower())
    def all(self) -> tuple[Capability, ...]: return tuple(self._items.values())
