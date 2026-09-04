"""Permission boundary for gesture capabilities."""
from __future__ import annotations


class GesturePermissions:
    """Deny gesture capabilities by default until explicitly enabled."""

    def __init__(self) -> None:
        self._grants: dict[str, set[str]] = {}

    def grant(self, principal: str, capability: str) -> None:
        self._grants.setdefault(principal, set()).add(capability)

    def revoke(self, principal: str, capability: str) -> None:
        self._grants.get(principal, set()).discard(capability)

    def allowed(self, principal: str, capability: str) -> bool:
        return capability in self._grants.get(principal, set())
