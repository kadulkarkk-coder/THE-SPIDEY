"""Coordinate widget lifecycle and layout without owning a UI toolkit."""
from __future__ import annotations

from .widget_framework import Widget
from .widget_layout import WidgetLayout
from .widget_registry import WidgetRegistry
from .widget_types import WidgetPosition


class WidgetController:
    """Safe orchestration layer for desktop widgets."""

    def __init__(self, *, registry: WidgetRegistry | None = None,
                 layout: WidgetLayout | None = None) -> None:
        self.registry = registry or WidgetRegistry()
        self.layout = layout or WidgetLayout()

    def register(self, widget: Widget, *, position: WidgetPosition | None = None) -> None:
        self.registry.register(widget)
        if position is not None:
            self.layout.set_position(widget.spec.widget_id, position)

    def show(self, widget_id: str):
        return self._require(widget_id).show()

    def hide(self, widget_id: str):
        return self._require(widget_id).hide()

    def minimize(self, widget_id: str):
        return self._require(widget_id).minimize()

    def move(self, widget_id: str, position: WidgetPosition) -> WidgetPosition:
        widget = self._require(widget_id)
        if not widget.spec.movable:
            raise PermissionError(f"widget is not movable: {widget_id}")
        return self.layout.set_position(widget_id, position)

    def resize(self, widget_id: str, position: WidgetPosition) -> WidgetPosition:
        widget = self._require(widget_id)
        if not widget.spec.resizable:
            raise PermissionError(f"widget is not resizable: {widget_id}")
        return self.layout.set_position(widget_id, position)

    def snapshots(self) -> dict[str, dict[str, object]]:
        return {widget.spec.widget_id: widget.snapshot() for widget in self.registry.list()}

    def _require(self, widget_id: str) -> Widget:
        widget = self.registry.get(widget_id)
        if widget is None:
            raise KeyError(f"unknown widget: {widget_id}")
        return widget
