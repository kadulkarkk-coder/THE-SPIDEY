"""Bounded conversation model for the WEBSTER UI."""
from __future__ import annotations

from .chat_types import ChatMessage, MessageRole


class ChatModel:
    """Maintain a compact display history; AI reasoning remains elsewhere."""

    def __init__(self, *, max_messages: int = 100) -> None:
        if max_messages < 1:
            raise ValueError("max_messages must be positive")
        self._max_messages = max_messages
        self._messages: list[ChatMessage] = []

    def add(self, role: MessageRole, text: str) -> ChatMessage:
        message = ChatMessage(role, text)
        self._messages.append(message)
        if len(self._messages) > self._max_messages:
            del self._messages[:-self._max_messages]
        return message

    def user(self, text: str) -> ChatMessage:
        return self.add(MessageRole.USER, text)

    def webster(self, text: str) -> ChatMessage:
        return self.add(MessageRole.WEBSTER, text)

    def snapshot(self) -> tuple[ChatMessage, ...]:
        return tuple(self._messages)

    def clear(self) -> None:
        self._messages.clear()
