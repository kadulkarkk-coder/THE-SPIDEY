"""Thread-safe widget registration and discovery boundary."""
from __future__ import annotations

from threading import RLock

from .widget_framework import Widget


class WidgetRegistry:
    """Register widget instances by stable ID and prevent accidental duplicates."""

    def __init__(self) -> None:
        self._widgets: dict[str, Widget] = {}
        self._lock = RLock()

    def register(self, widget: Widget, *, replace: bool = False) -> None:
        widget_id = widget.spec.widget_id
        with self._lock:
            if widget_id in self._widgets and not replace:
                raise ValueError(f"widget already registered: {widget_id}")
            self._widgets[widget_id] = widget

    def get(self, widget_id: str) -> Widget | None:
        with self._lock:
            return self._widgets.get(widget_id)

    def remove(self, widget_id: str) -> Widget | None:
        with self._lock:
            return self._widgets.pop(widget_id, None)

    def list(self) -> tuple[Widget, ...]:
        with self._lock:
            return tuple(self._widgets.values())
