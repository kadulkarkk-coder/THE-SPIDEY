"""Permissioned mouse action planner; does not inject pointer events."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class MouseAction:
    action: str
    x: int | None = None
    y: int | None = None
    button: str | None = None

class MouseInput:
    ACTIONS = frozenset({"move", "click", "double_click", "scroll"})
    def plan(self, action: str, *, x: int | None = None, y: int | None = None, button: str | None = None) -> MouseAction:
        value = action.strip().lower()
        if value not in self.ACTIONS: raise ValueError("unsupported mouse action")
        if value in {"move", "click", "double_click"} and (x is None or y is None): raise ValueError("coordinates are required")
        return MouseAction(value, x, y, button.strip().lower() if button else None)
