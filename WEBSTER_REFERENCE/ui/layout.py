"""Logical layout model for WEBSTER's desktop shell."""
from __future__ import annotations

from dataclasses import dataclass

from .ui_constants import HEADER_HEIGHT, SIDEBAR_WIDTH


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class ShellLayout:
    sidebar: Rect
    header: Rect
    content: Rect


def calculate_layout(width: int, height: int) -> ShellLayout:
    if width <= 0 or height <= 0:
        raise ValueError("window dimensions must be positive")
    sidebar_width = min(SIDEBAR_WIDTH, width)
    header_height = min(HEADER_HEIGHT, height)
    return ShellLayout(
        sidebar=Rect(0, 0, sidebar_width, height),
        header=Rect(sidebar_width, 0, width - sidebar_width, header_height),
        content=Rect(sidebar_width, header_height, width - sidebar_width, height - header_height),
    )
