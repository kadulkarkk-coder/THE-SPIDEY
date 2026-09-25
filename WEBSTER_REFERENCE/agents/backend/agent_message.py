"""Structured messages exchanged between agents."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

@dataclass(frozen=True)
class AgentMessage:
    sender: str
    recipient: str
    task: str
    payload: Any = None
    timestamp: datetime = None

    @classmethod
    def create(cls, sender: str, recipient: str, task: str, payload: Any = None):
        return cls(sender.strip(), recipient.strip(), task.strip(), payload, datetime.now(timezone.utc))
