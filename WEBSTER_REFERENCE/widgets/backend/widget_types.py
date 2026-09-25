"""Provider-neutral contracts for WEBSTER desktop widgets."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class WidgetState(str, Enum):
    HIDDEN = "hidden"
    VISIBLE = "visible"
    MINIMIZED = "minimized"
    ERROR = "error"


@dataclass(frozen=True)
class WidgetSpec:
    """Stable metadata describing a widget without binding to a UI toolkit."""
    widget_id: str
    title: str
    category: str = "general"
    resizable: bool = True
    movable: bool = True
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.widget_id.strip():
            raise ValueError("widget_id must not be empty")
        if not self.title.strip():
            raise ValueError("title must not be empty")


@dataclass(frozen=True)
class WidgetEvent:
    widget_id: str
    state: WidgetState
    message: str = ""


@dataclass(frozen=True)
class WidgetPosition:
    x: int = 0
    y: int = 0
    width: int = 320
    height: int = 180

    def __post_init__(self) -> None:
        if self.width < 1 or self.height < 1:
            raise ValueError("widget dimensions must be positive")
