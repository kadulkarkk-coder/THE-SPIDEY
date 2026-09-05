"""Toolkit-neutral main window model for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass

from .layout import ShellLayout, calculate_layout


@dataclass(frozen=True)
class WindowSnapshot:
    title: str
    width: int
    height: int
    layout: ShellLayout


class MainWindow:
    """Represent the desktop shell without creating a native window."""

    def __init__(self, *, title: str = "WEBSTER", width: int = 1280, height: int = 800) -> None:
        self.title = title
        self._width = width
        self._height = height

    def resize(self, width: int, height: int) -> WindowSnapshot:
        layout = calculate_layout(width, height)
        self._width, self._height = width, height
        return WindowSnapshot(self.title, width, height, layout)

    def snapshot(self) -> WindowSnapshot:
        return WindowSnapshot(self.title, self._width, self._height, calculate_layout(self._width, self._height))
