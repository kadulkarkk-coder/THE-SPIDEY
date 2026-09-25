"""Local clock widget with no polling thread or external dependency."""
from __future__ import annotations

from datetime import datetime

from .widget_framework import Widget
from .widget_types import WidgetSpec


class ClockWidget(Widget):
    """Render current local time only when its snapshot is requested."""

    def __init__(self) -> None:
        super().__init__(WidgetSpec("clock", "Clock", category="utility", resizable=False))

    def snapshot(self) -> dict[str, object]:
        now = datetime.now().astimezone()
        return {"widget_id": self.spec.widget_id, "time": now.strftime("%H:%M:%S"),
                "date": now.strftime("%Y-%m-%d"), "timezone": str(now.tzinfo),
                "state": self.state.value}
