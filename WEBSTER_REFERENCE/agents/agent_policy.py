"""Policy checks for safe agent delegation."""
from __future__ import annotations

class AgentPolicy:
    def __init__(self, blocked_capabilities: set[str] | None = None): self.blocked = {x.lower() for x in (blocked_capabilities or set())}
    def allowed(self, capability: str) -> bool: return capability.strip().lower() not in self.blocked
