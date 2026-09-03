"""Permissioned keyboard action planner; does not inject keystrokes."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class KeyAction:
    key: str
    modifiers: tuple[str, ...] = ()

class KeyboardInput:
    def plan(self, key: str, modifiers: tuple[str, ...] = ()) -> KeyAction:
        value = key.strip()
        mods = tuple(m.strip().lower() for m in modifiers if m.strip())
        if not value: raise ValueError("key is required")
        return KeyAction(value, mods)
