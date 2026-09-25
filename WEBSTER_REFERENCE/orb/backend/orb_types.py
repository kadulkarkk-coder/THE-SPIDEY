"""Lightweight contracts for the WEBSTER desktop Floating Orb."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from time import monotonic


class OrbState(str, Enum):
    HIDDEN = "hidden"
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    ACTING = "acting"
    ERROR = "error"


@dataclass(frozen=True)
class OrbEvent:
    state: OrbState
    message: str = ""
    timestamp: float = field(default_factory=monotonic)


@dataclass(frozen=True)
class OrbAction:
    name: str
    value: str = ""
