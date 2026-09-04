"""Coordinate UI state without binding WEBSTER to a GUI toolkit."""
from __future__ import annotations

from .ui_state import UIState
from .ui_types import UIEvent, UITheme, ViewState


class UIController:
    """Expose simple navigation and theme operations to future renderers."""

    def __init__(self, state: UIState | None = None) -> None:
        self.state = state or UIState()

    def show(self, view: str) -> UIEvent:
        self.state.set_view(view, ViewState.VISIBLE)
        return UIEvent("show", view, "Visible", ViewState.VISIBLE)

    def hide(self, view: str) -> UIEvent:
        self.state.set_view(view, ViewState.HIDDEN)
        return UIEvent("hide", view, "Hidden", ViewState.HIDDEN)

    def minimize(self, view: str) -> UIEvent:
        self.state.set_view(view, ViewState.MINIMIZED)
        return UIEvent("minimize", view, "Minimized", ViewState.MINIMIZED)

    def set_theme(self, theme: UITheme) -> UITheme:
        self.state.set_theme(theme)
        return theme

    def snapshot(self) -> dict[str, object]:
        return self.state.snapshot()
