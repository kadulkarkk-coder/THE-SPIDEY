"""Provider-neutral remote message envelope for phone communication."""
from __future__ import annotations

from dataclasses import dataclass
from secrets import token_urlsafe
from time import time


@dataclass(frozen=True)
class SecureMessage:
    message_id: str
    device_id: str
    session_id: str
    kind: str
    payload: str
    created_at: float


class SecureMessageFactory:
    """Create authenticated-session-bound message envelopes without handling transport."""

    def create(self, device_id: str, session_id: str, kind: str, payload: str) -> SecureMessage:
        device_id = device_id.strip()
        session_id = session_id.strip()
        kind = kind.strip()
        if not device_id or not session_id or not kind:
            raise ValueError("device_id, session_id, and kind must not be empty")
        if not payload:
            raise ValueError("payload must not be empty")
        return SecureMessage(token_urlsafe(16), device_id, session_id, kind, payload, time())
