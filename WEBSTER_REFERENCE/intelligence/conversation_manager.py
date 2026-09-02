"""Bounded conversation state for WEBSTER intelligence."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from threading import RLock


@dataclass(frozen=True)
class ConversationTurn:
    role: str
    text: str
    timestamp: datetime


class ConversationManager:
    """Maintains a bounded, inspectable conversation history."""

    def __init__(self, max_turns: int = 20) -> None:
        if max_turns < 1:
            raise ValueError("max_turns must be at least 1")
        self.max_turns = max_turns
        self._turns: list[ConversationTurn] = []
        self._lock = RLock()

    def add(self, role: str, text: str) -> ConversationTurn:
        role = role.strip().lower()
        text = " ".join(text.split())
        if not role or not text:
            raise ValueError("role and text are required")
        turn = ConversationTurn(role, text, datetime.now(timezone.utc))
        with self._lock:
            self._turns.append(turn)
            del self._turns[:-self.max_turns]
        return turn

    def history(self) -> tuple[ConversationTurn, ...]:
        with self._lock:
            return tuple(self._turns)

    def clear(self) -> None:
        with self._lock:
            self._turns.clear()

    def size(self) -> int:
        return len(self.history())
