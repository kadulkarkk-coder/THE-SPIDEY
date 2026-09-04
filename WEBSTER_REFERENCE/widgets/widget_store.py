"""Bounded in-memory widget data store for low-overhead runtime use."""
from __future__ import annotations

from threading import RLock

from .widget_data import WidgetData


class WidgetDataStore:
    """Keep the latest payload per widget without creating background workers."""

    def __init__(self) -> None:
        self._data: dict[str, WidgetData] = {}
        self._lock = RLock()

    def set(self, widget_id: str, data: WidgetData) -> WidgetData:
        if not widget_id.strip():
            raise ValueError("widget_id must not be empty")
        with self._lock:
            self._data[widget_id] = data
        return data

    def get(self, widget_id: str) -> WidgetData | None:
        with self._lock:
            return self._data.get(widget_id)

    def remove(self, widget_id: str) -> WidgetData | None:
        with self._lock:
            return self._data.pop(widget_id, None)

    def snapshot(self) -> dict[str, WidgetData]:
        with self._lock:
            return dict(self._data)
