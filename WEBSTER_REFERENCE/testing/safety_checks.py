"""Safety-oriented checks for permission-aware WEBSTER subsystems."""
from __future__ import annotations

from .contract_checks import require


def check_permission_boundary(permission_system: object, principal: str, capability: str) -> None:
    """Require permission systems to return an explicit boolean decision."""
    allowed = getattr(permission_system, "allowed", None)
    require(callable(allowed), "permission system must expose allowed()")
    decision = allowed(principal, capability)
    require(isinstance(decision, bool), "permission decision must be boolean")


def check_risk_level(level: object) -> None:
    """Reject empty or malformed risk labels before execution tests."""
    require(isinstance(level, str) and bool(level.strip()), "risk level must be non-empty text")
