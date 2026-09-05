"""High-level composition of WEBSTER's first desktop UI shell."""
from __future__ import annotations

from dataclasses import dataclass

from .dashboard import Dashboard
from .layout import ShellLayout, calculate_layout
from .ui_manifest import DEFAULT_VIEWS, UIViewSpec


@dataclass(frozen=True)
class ShellSnapshot:
    active_view: str
    layout: ShellLayout
    views: tuple[UIViewSpec, ...]
    dashboard: tuple


class UIShell:
    """Compose navigation-level UI pieces without depending on a GUI toolkit."""

    def __init__(self, *, width: int = 1280, height: int = 800) -> None:
        self.width = width
        self.height = height
        self.active_view = "home"
        self.views = DEFAULT_VIEWS
        self.dashboard = Dashboard()

    def navigate(self, view_id: str) -> str:
        if view_id not in {view.view_id for view in self.views}:
            raise ValueError(f"unknown UI view: {view_id}")
        self.active_view = view_id
        return view_id

    def resize(self, width: int, height: int) -> ShellLayout:
        layout = calculate_layout(width, height)
        self.width, self.height = width, height
        return layout

    def snapshot(self) -> ShellSnapshot:
        return ShellSnapshot(self.active_view, calculate_layout(self.width, self.height), self.views, self.dashboard.snapshot())
