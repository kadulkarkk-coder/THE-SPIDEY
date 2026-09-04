"""Observable voice lifecycle events."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class VoiceEvent:
    event: str
    detail: str = ""
    timestamp: datetime | None = None

class VoiceEventLog:
    def __init__(self, max_events: int = 200) -> None:
        self.max_events = max(1, max_events)
        self._events: list[VoiceEvent] = []

    def emit(self, event: str, detail: str = "") -> VoiceEvent:
        name = event.strip().lower()
        if not name:
            raise ValueError("event is required")
        item = VoiceEvent(name, detail.strip(), datetime.now(timezone.utc))
        self._events.append(item)
        del self._events[:-self.max_events]
        return item

    def recent(self, limit: int = 20) -> tuple[VoiceEvent, ...]:
        return tuple(self._events[-max(1, limit):])
