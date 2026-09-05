"""Provider-neutral contracts for the WEBSTER conversation surface."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from time import time


class MessageRole(str, Enum):
    USER = "user"
    WEBSTER = "webster"
    SYSTEM = "system"


@dataclass(frozen=True)
class ChatMessage:
    role: MessageRole
    text: str
    timestamp: float = 0.0

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("message text must not be empty")
        if self.timestamp == 0.0:
            object.__setattr__(self, "timestamp", time())
