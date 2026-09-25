"""Compact layout model for movable and resizable desktop widgets."""
from __future__ import annotations

from threading import RLock

from .widget_types import WidgetPosition


class WidgetLayout:
    """Keep layout state separate from any desktop UI toolkit."""

    def __init__(self) -> None:
        self._positions: dict[str, WidgetPosition] = {}
        self._lock = RLock()

    def set_position(self, widget_id: str, position: WidgetPosition) -> WidgetPosition:
        if not widget_id.strip():
            raise ValueError("widget_id must not be empty")
        with self._lock:
            self._positions[widget_id] = position
        return position

    def get_position(self, widget_id: str) -> WidgetPosition | None:
        with self._lock:
            return self._positions.get(widget_id)

    def snapshot(self) -> dict[str, WidgetPosition]:
        with self._lock:
            return dict(self._positions)

    def remove(self, widget_id: str) -> None:
        with self._lock:
            self._positions.pop(widget_id, None)
