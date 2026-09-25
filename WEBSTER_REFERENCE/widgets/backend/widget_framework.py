"""Lightweight, provider-neutral desktop widget framework."""
from __future__ import annotations

from abc import ABC, abstractmethod

from .widget_types import WidgetEvent, WidgetSpec, WidgetState


class Widget(ABC):
    """Base contract for a desktop widget implementation."""

    spec: WidgetSpec

    def __init__(self, spec: WidgetSpec) -> None:
        self.spec = spec
        self._state = WidgetState.HIDDEN

    @property
    def state(self) -> WidgetState:
        return self._state

    def show(self) -> WidgetEvent:
        self._state = WidgetState.VISIBLE
        return WidgetEvent(self.spec.widget_id, self._state, "Visible")

    def hide(self) -> WidgetEvent:
        self._state = WidgetState.HIDDEN
        return WidgetEvent(self.spec.widget_id, self._state, "Hidden")

    def minimize(self) -> WidgetEvent:
        self._state = WidgetState.MINIMIZED
        return WidgetEvent(self.spec.widget_id, self._state, "Minimized")

    def fail(self, message: str) -> WidgetEvent:
        self._state = WidgetState.ERROR
        return WidgetEvent(self.spec.widget_id, self._state, message)

    @abstractmethod
    def snapshot(self) -> dict[str, object]:
        """Return small serializable state for a renderer or sync layer."""
        raise NotImplementedError
