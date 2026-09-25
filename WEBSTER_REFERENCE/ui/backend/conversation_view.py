"""Conversation workspace model for the WEBSTER desktop UI."""
from __future__ import annotations

from dataclasses import dataclass

from .chat_controller import ChatController
from .chat_types import ChatMessage


@dataclass(frozen=True)
class ComposerState:
    text: str = ""
    enabled: bool = True


class ConversationView:
    """Toolkit-neutral chat surface with a separate message composer."""

    def __init__(self, controller: ChatController | None = None) -> None:
        self.controller = controller or ChatController()
        self.composer = ComposerState()

    def submit(self, text: str) -> ChatMessage:
        return self.controller.submit_user(text)

    def receive(self, text: str) -> ChatMessage:
        return self.controller.append_webster(text)

    def messages(self) -> tuple[ChatMessage, ...]:
        return self.controller.messages()

    def clear(self) -> None:
        self.controller.clear()
