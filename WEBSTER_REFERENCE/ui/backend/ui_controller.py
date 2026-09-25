"""Coordinate UI state and emit presentation events."""
from __future__ import annotations

from .ui_events import UIActionEvent, UIEventBus
from .ui_state import UIState
from .ui_types import UIEvent, UITheme, ViewState


class UIController:
    """Expose navigation, theme, and runtime-facing UI actions."""

    def __init__(self, state: UIState | None = None, events: UIEventBus | None = None) -> None:
        self.state = state or UIState()
        self.events = events or UIEventBus()

    def show(self, view: str) -> UIEvent:
        self.state.set_view(view, ViewState.VISIBLE)
        event = UIEvent("show", view, "Visible", ViewState.VISIBLE)
        self.events.emit(UIActionEvent("view.show", payload={"view": view}))
        return event

    def hide(self, view: str) -> UIEvent:
        self.state.set_view(view, ViewState.HIDDEN)
        event = UIEvent("hide", view, "Hidden", ViewState.HIDDEN)
        self.events.emit(UIActionEvent("view.hide", payload={"view": view}))
        return event

    def minimize(self, view: str) -> UIEvent:
        self.state.set_view(view, ViewState.MINIMIZED)
        event = UIEvent("minimize", view, "Minimized", ViewState.MINIMIZED)
        self.events.emit(UIActionEvent("view.minimize", payload={"view": view}))
        return event

    def submit_command(self, command: str) -> UIActionEvent:
        if not command.strip():
            raise ValueError("command must not be empty")
        event = UIActionEvent("command.submit", payload={"command": command.strip()})
        self.events.emit(event)
        return event

    def set_theme(self, theme: UITheme) -> UITheme:
        self.state.set_theme(theme)
        self.events.emit(UIActionEvent("theme.change", payload={"theme": theme.name}))
        return theme

    def snapshot(self) -> dict[str, object]:
        return self.state.snapshot()
