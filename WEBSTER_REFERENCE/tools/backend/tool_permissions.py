"""Explicit allow/deny permissions for tool capabilities."""
from __future__ import annotations

class ToolPermissionPolicy:
    def __init__(self) -> None:
        self._allowed: dict[str, set[str]] = {}
        self._denied: dict[str, set[str]] = {}

    def allow(self, principal: str, capability: str) -> None:
        self._allowed.setdefault(principal.strip().lower(), set()).add(capability.strip().lower())

    def deny(self, principal: str, capability: str) -> None:
        self._denied.setdefault(principal.strip().lower(), set()).add(capability.strip().lower())

    def permitted(self, principal: str, capability: str) -> bool:
        p, c = principal.strip().lower(), capability.strip().lower()
        if c in self._denied.get(p, set()): return False
        return c in self._allowed.get(p, set())
