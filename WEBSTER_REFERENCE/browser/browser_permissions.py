"""Permission boundary for browser capabilities."""
from __future__ import annotations

class BrowserPermissions:
    def __init__(self) -> None: self._grants: dict[str, set[str]] = {}
    def grant(self, principal: str, capability: str) -> None:
        self._grants.setdefault(principal.strip(), set()).add(capability.strip())
    def revoke(self, principal: str, capability: str) -> None:
        self._grants.get(principal.strip(), set()).discard(capability.strip())
    def allowed(self, principal: str, capability: str) -> bool:
        return capability.strip() in self._grants.get(principal.strip(), set())
