"""Deterministic, bounded context construction for WEBSTER requests."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .conversation_state import ConversationState, ConversationTurn


@dataclass(frozen=True)
class BuiltContext:
    """Compact context passed to the response layer."""

    prompt: str
    recent_turns: tuple[ConversationTurn, ...]
    runtime: dict[str, Any]


class ContextBuilder:
    """Builds only the context needed for one response; never performs inference."""

    def __init__(self, max_prompt_chars: int = 1600, max_runtime_items: int = 12) -> None:
        self.max_prompt_chars = max_prompt_chars
        self.max_runtime_items = max_runtime_items

    def build(
        self,
        prompt: str,
        conversation: ConversationState,
        runtime: dict[str, Any] | None = None,
    ) -> BuiltContext:
        cleaned = " ".join(prompt.split())[: self.max_prompt_chars]
        runtime_data = dict(runtime or {})
        runtime_data = dict(list(runtime_data.items())[: self.max_runtime_items])
        return BuiltContext(cleaned, conversation.recent(), runtime_data)

    @staticmethod
    def as_prompt(context: BuiltContext) -> str:
        """Render a bounded human-readable context without exposing internals."""
        lines = [f"Current request: {context.prompt}"]
        if context.recent_turns:
            lines.append("Recent conversation:")
            for turn in context.recent_turns:
                lines.append(f"{turn.role}: {turn.text}")
        return "\n".join(lines)
