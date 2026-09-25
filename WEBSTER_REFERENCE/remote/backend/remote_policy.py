"""Safety policy for WEBSTER Anywhere requests."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RemotePolicy:
    """Conservative defaults for commands arriving from a phone."""

    allow_chat: bool = True
    allow_calls: bool = True
    require_confirmation_for_sensitive: bool = True

    def allowed(self, channel: str) -> bool:
        channel = channel.strip().lower()
        if channel == "chat":
            return self.allow_chat
        if channel == "call":
            return self.allow_calls
        return False

    def requires_confirmation(self, sensitive: bool) -> bool:
        return sensitive and self.require_confirmation_for_sensitive
