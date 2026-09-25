"""Policy checks that gate reasoning outcomes before action."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str
    rule: str


class PolicyReasoner:
    """Provides simple deterministic allow/deny decisions."""

    def evaluate(self, action: str, *, permitted: bool = True, requires_confirmation: bool = False) -> PolicyDecision:
        action = " ".join(action.split())
        if not action:
            return PolicyDecision(False, "action is empty", "non_empty_action")
        if not permitted:
            return PolicyDecision(False, "action is not permitted", "permission")
        if requires_confirmation:
            return PolicyDecision(False, "confirmation is required before execution", "confirmation")
        return PolicyDecision(True, "action passed policy checks", "default_allow")
