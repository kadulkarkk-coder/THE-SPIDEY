"""Provider-neutral contracts for the WEBSTER desktop UI."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class ViewState(str, Enum):
    HIDDEN = "hidden"
    VISIBLE = "visible"
    MINIMIZED = "minimized"


@dataclass(frozen=True)
class UITheme:
    """Theme tokens without coupling to a specific rendering toolkit."""
    name: str = "webster-dark"
    background: str = "#0b1020"
    foreground: str = "#f4f7ff"
    accent: str = "#7c5cff"
    surface: str = "#151b2e"
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class UIEvent:
    name: str
    view: str = "main"
    message: str = ""
    state: ViewState = ViewState.VISIBLE
