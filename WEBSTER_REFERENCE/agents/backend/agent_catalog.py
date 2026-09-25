"""Catalog and metadata for the built-in agent roles."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class AgentDescriptor:
    name: str
    capabilities: tuple[str, ...]
    description: str = ""

class AgentCatalog:
    def __init__(self): self._items: dict[str, AgentDescriptor] = {}
    def register(self, descriptor: AgentDescriptor) -> None: self._items[descriptor.name.lower()] = descriptor
    def get(self, name: str) -> AgentDescriptor | None: return self._items.get(name.lower())
    def all(self) -> tuple[AgentDescriptor, ...]: return tuple(self._items.values())
