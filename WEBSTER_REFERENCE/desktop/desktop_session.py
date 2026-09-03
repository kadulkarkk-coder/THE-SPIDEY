"""Controlled desktop interaction session state."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from threading import RLock

@dataclass(frozen=True)
class DesktopSession:
    session_id: str
    principal: str
    active: bool = True
    started_at: datetime | None = None

class DesktopSessionManager:
    def __init__(self) -> None:
        self._sessions: dict[str, DesktopSession] = {}
        self._lock = RLock()

    def open(self, session_id: str, principal: str = "user") -> DesktopSession:
        sid, who = session_id.strip(), principal.strip()
        if not sid or not who: raise ValueError("session_id and principal are required")
        item = DesktopSession(sid, who, True, datetime.now(timezone.utc))
        with self._lock: self._sessions[sid] = item
        return item

    def get(self, session_id: str) -> DesktopSession | None:
        with self._lock: return self._sessions.get(session_id.strip())

    def close(self, session_id: str) -> bool:
        with self._lock:
            current = self._sessions.get(session_id.strip())
            if not current: return False
            self._sessions[current.session_id] = DesktopSession(current.session_id, current.principal, False, current.started_at)
            return True
