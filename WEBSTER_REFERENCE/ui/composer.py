"""Input composer model for the WEBSTER conversation UI."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComposerSnapshot:
    text: str
    enabled: bool


class Composer:
    """Manage draft input without coupling submission to a GUI toolkit."""

    def __init__(self) -> None:
        self._text = ""
        self._enabled = True

    def set_text(self, text: str) -> ComposerSnapshot:
        self._text = text
        return self.snapshot()

    def append(self, text: str) -> ComposerSnapshot:
        self._text += text
        return self.snapshot()

    def clear(self) -> ComposerSnapshot:
        self._text = ""
        return self.snapshot()

    def set_enabled(self, enabled: bool) -> ComposerSnapshot:
        self._enabled = bool(enabled)
        return self.snapshot()

    def can_submit(self) -> bool:
        return self._enabled and bool(self._text.strip())

    def consume(self) -> str:
        if not self.can_submit():
            raise ValueError("composer is disabled or empty")
        text = self._text.strip()
        self._text = ""
        return text

    def snapshot(self) -> ComposerSnapshot:
        return ComposerSnapshot(self._text, self._enabled)
