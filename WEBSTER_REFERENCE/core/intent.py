"""Lightweight intent parsing for the WEBSTER runtime.

This is deliberately deterministic: it identifies a command name and arguments
without pretending to perform natural-language understanding yet.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedIntent:
    name: str
    arguments: tuple[str, ...]
    raw_text: str

    @property
    def has_arguments(self) -> bool:
        return bool(self.arguments)


def parse_intent(text: str) -> ParsedIntent:
    raw = text.strip()
    parts = tuple(raw.split())
    if not parts:
        return ParsedIntent("", (), raw)
    return ParsedIntent(parts[0].lower(), parts[1:], raw)
