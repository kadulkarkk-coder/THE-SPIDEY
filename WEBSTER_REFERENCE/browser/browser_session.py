"""Controlled browser session state without launching a browser."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlparse

@dataclass(frozen=True)
class BrowserSession:
    session_id: str
    url: str | None = None
    title: str | None = None
    active: bool = True
    updated_at: datetime = None

class BrowserSessionManager:
    def __init__(self) -> None: self._sessions: dict[str, BrowserSession] = {}
    def open(self, session_id: str, url: str | None = None) -> BrowserSession:
        if not session_id.strip(): raise ValueError("session_id is required")
        if url and not urlparse(url).scheme: raise ValueError("url must include a scheme")
        item = BrowserSession(session_id.strip(), url, None, True, datetime.now(timezone.utc))
        self._sessions[item.session_id] = item
        return item
    def update(self, session_id: str, *, url: str | None = None, title: str | None = None) -> BrowserSession:
        current = self._sessions[session_id.strip()]
        item = BrowserSession(current.session_id, url or current.url, title or current.title, current.active, datetime.now(timezone.utc))
        self._sessions[item.session_id] = item
        return item
    def close(self, session_id: str) -> bool:
        current = self._sessions.get(session_id.strip())
        if not current: return False
        self._sessions[current.session_id] = BrowserSession(current.session_id, current.url, current.title, False, datetime.now(timezone.utc))
        return True
