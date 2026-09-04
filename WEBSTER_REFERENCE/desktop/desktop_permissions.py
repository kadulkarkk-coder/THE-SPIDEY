"""Capability permissions for desktop operations."""
from __future__ import annotations

class DesktopPermissions:
    def __init__(self) -> None:
        self._grants: dict[str, set[str]] = {}

    def grant(self, principal: str, capability: str) -> None:
        who, cap = principal.strip(), capability.strip().lower()
        if not who or not cap:
            raise ValueError("principal and capability are required")
        self._grants.setdefault(who, set()).add(cap)

    def revoke(self, principal: str, capability: str) -> None:
        self._grants.get(principal.strip(), set()).discard(capability.strip().lower())

    def allowed(self, principal: str, capability: str) -> bool:
        return capability.strip().lower() in self._grants.get(principal.strip(), set())
