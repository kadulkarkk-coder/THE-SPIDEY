"""Coordinate conversation UI state without owning an AI provider."""
from __future__ import annotations

from .chat_model import ChatModel
from .chat_types import ChatMessage


class ChatController:
    """Accept display messages and expose bounded conversation state."""

    def __init__(self, model: ChatModel | None = None) -> None:
        self.model = model or ChatModel()

    def submit_user(self, text: str) -> ChatMessage:
        return self.model.user(text)

    def append_webster(self, text: str) -> ChatMessage:
        return self.model.webster(text)

    def messages(self) -> tuple[ChatMessage, ...]:
        return self.model.snapshot()

    def clear(self) -> None:
        self.model.clear()
