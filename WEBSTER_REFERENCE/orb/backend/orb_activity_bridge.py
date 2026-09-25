"""Bridge Orb activity into WEBSTER memory without coupling to a UI."""
from __future__ import annotations

from .orb_activity_log import OrbActivityLog


class OrbActivityBridge:
    """Record important Orb interaction messages in a supplied memory manager."""

    def __init__(self, memory, log: OrbActivityLog | None = None) -> None:
        self.memory = memory
        self.log = log or OrbActivityLog()

    def record(self, message: str, *, event: str = "interaction"):
        entry = self.log.append(event, message)
        return self.memory.remember(
            f"orb:{entry.timestamp:.6f}",
            message,
            kind="orb_activity",
            sensitive=False,
        )
