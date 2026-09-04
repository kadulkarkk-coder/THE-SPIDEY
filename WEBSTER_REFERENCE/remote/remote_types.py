"""Provider-neutral contracts for WEBSTER Anywhere remote control."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from time import monotonic
from typing import Mapping


class RemoteChannel(str, Enum):
    CHAT = "chat"
    CALL = "call"


class RemoteStatus(str, Enum):
    OFFLINE = "offline"
    CONNECTING = "connecting"
    ONLINE = "online"
    BUSY = "busy"


@dataclass(frozen=True)
class RemoteRequest:
    """A small command envelope sent from the phone to the laptop."""

    request_id: str
    channel: RemoteChannel
    text: str
    device_id: str
    timestamp: float = field(default_factory=monotonic)
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id must not be empty")
        if not self.device_id.strip():
            raise ValueError("device_id must not be empty")
        if not self.text.strip():
            raise ValueError("text must not be empty")


@dataclass(frozen=True)
class RemoteResponse:
    """Result returned to the phone without exposing internal state."""

    request_id: str
    ok: bool
    text: str
    status: RemoteStatus
