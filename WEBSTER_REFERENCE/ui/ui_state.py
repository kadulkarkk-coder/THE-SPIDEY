"""Thread-safe UI state boundary for WEBSTER."""
from __future__ import annotations

from threading import RLock

from .ui_types import UITheme, ViewState


class UIState:
    """Store only presentation state; rendering remains outside the core."""

    def __init__(self, *, theme: UITheme | None = None) -> None:
        self._view_states: dict[str, ViewState] = {}
        self._theme = theme or UITheme()
        self._lock = RLock()

    def set_view(self, view: str, state: ViewState) -> None:
        if not view.strip():
            raise ValueError("view must not be empty")
        with self._lock:
            self._view_states[view] = state

    def view_state(self, view: str) -> ViewState:
        with self._lock:
            return self._view_states.get(view, ViewState.HIDDEN)

    def set_theme(self, theme: UITheme) -> None:
        with self._lock:
            self._theme = theme

    def theme(self) -> UITheme:
        with self._lock:
            return self._theme

    def snapshot(self) -> dict[str, object]:
        with self._lock:
            return {"views": dict(self._view_states), "theme": self._theme}
