"""Map normalized gestures to logical, provider-independent actions."""
from __future__ import annotations

from .gesture_types import GestureAction, GestureKind


class GestureMapper:
    """Keep gesture-to-action policy explicit and easy to replace."""

    DEFAULT_MAP = {
        GestureKind.TAP: "select",
        GestureKind.SWIPE_LEFT: "navigate_previous",
        GestureKind.SWIPE_RIGHT: "navigate_next",
        GestureKind.SWIPE_UP: "scroll_up",
        GestureKind.SWIPE_DOWN: "scroll_down",
        GestureKind.PINCH: "zoom",
        GestureKind.OPEN_PALM: "pause",
        GestureKind.FIST: "cancel",
    }

    def __init__(self, mapping: dict[GestureKind, str] | None = None) -> None:
        self._mapping = dict(mapping or self.DEFAULT_MAP)

    def map(self, gesture: GestureKind) -> GestureAction | None:
        action = self._mapping.get(gesture)
        return GestureAction(action) if action else None
