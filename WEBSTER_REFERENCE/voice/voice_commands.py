"""Normalize spoken text into lightweight voice commands."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class VoiceCommand:
    name: str
    arguments: tuple[str, ...]
    raw_text: str

class VoiceCommandParser:
    def parse(self, text: str) -> VoiceCommand:
        raw = " ".join(text.split())
        parts = tuple(raw.split())
        if not parts:
            return VoiceCommand("", (), raw)
        return VoiceCommand(parts[0].lower(), parts[1:], raw)
