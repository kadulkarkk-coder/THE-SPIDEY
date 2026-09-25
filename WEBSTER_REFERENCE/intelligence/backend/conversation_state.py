"""Session-scoped conversation state for WEBSTER's local intelligence layer."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from threading import RLock
from uuid import uuid4


@dataclass(frozen=True)
class ConversationTurn:
    """A normalized turn retained for contextual reasoning."""

    role: str
    text: str
    timestamp: datetime


class ConversationState:
    """Bounded session state with deterministic limits and thread-safe access."""

    def __init__(self, max_turns: int = 12, max_chars_per_turn: int = 1200) -> None:
        if max_turns < 1 or max_chars_per_turn < 1:
            raise ValueError("conversation limits must be positive")
        self.max_turns = max_turns
        self.max_chars_per_turn = max_chars_per_turn
        self.session_id = uuid4().hex
        self._turns: list[ConversationTurn] = []
        self._lock = RLock()

    def add(self, role: str, text: str) -> ConversationTurn:
        role = role.strip().lower()
        text = " ".join(text.split())[: self.max_chars_per_turn]
        if not role or not text:
            raise ValueError("role and text are required")
        turn = ConversationTurn(role, text, datetime.now(timezone.utc))
        with self._lock:
            self._turns.append(turn)
            del self._turns[:-self.max_turns]
        return turn

    def recent(self) -> tuple[ConversationTurn, ...]:
        with self._lock:
            return tuple(self._turns)

    def clear(self) -> None:
        with self._lock:
            self._turns.clear()

    def size(self) -> int:
        with self._lock:
            return len(self._turns)
