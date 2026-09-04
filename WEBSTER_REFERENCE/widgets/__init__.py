"""WEBSTER Desktop Widgets reference package."""

from .clock_widget import ClockWidget
from .widget_data import WidgetData, WidgetDataError
from .widget_store import WidgetDataStore

__all__ = ["ClockWidget", "WidgetData", "WidgetDataError", "WidgetDataStore"]
