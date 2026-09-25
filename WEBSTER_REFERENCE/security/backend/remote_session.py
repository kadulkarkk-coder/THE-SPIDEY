"""Authenticated remote-session state for phone-to-WEBSTER communication."""
from __future__ import annotations

from dataclasses import dataclass
from secrets import token_urlsafe
from time import time


@dataclass(frozen=True)
class RemoteSession:
    session_id: str
    device_id: str
    created_at: float
    expires_at: float


class RemoteSessionManager:
    """Manage short-lived sessions; transport encryption belongs to the gateway."""

    def __init__(self, *, ttl_seconds: int = 3600) -> None:
        if ttl_seconds < 60:
            raise ValueError("ttl_seconds must be at least 60")
        self.ttl_seconds = ttl_seconds
        self._sessions: dict[str, RemoteSession] = {}

    def open(self, device_id: str) -> RemoteSession:
        device_id = device_id.strip()
        if not device_id:
            raise ValueError("device_id must not be empty")
        now = time()
        session = RemoteSession(token_urlsafe(24), device_id, now, now + self.ttl_seconds)
        self._sessions[session.session_id] = session
        return session

    def valid(self, session_id: str, device_id: str) -> bool:
        session = self._sessions.get(session_id)
        return bool(session and session.device_id == device_id.strip() and time() <= session.expires_at)

    def revoke(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
