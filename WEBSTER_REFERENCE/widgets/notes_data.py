"""Local notes payload support for the desktop widget layer."""
from __future__ import annotations

from dataclasses import dataclass, field
from time import time


@dataclass(frozen=True)
class NoteItem:
    """A small note suitable for a local widget or later sync layer."""

    text: str
    created_at: float = field(default_factory=time)
    updated_at: float = field(default_factory=time)

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("note text must not be empty")
