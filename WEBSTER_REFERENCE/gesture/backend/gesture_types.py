"""Core data contracts for lightweight WEBSTER gesture input."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from time import monotonic
from typing import Mapping


class GestureKind(str, Enum):
    """Normalized gestures understood by the platform."""

    NONE = "none"
    TAP = "tap"
    SWIPE_LEFT = "swipe_left"
    SWIPE_RIGHT = "swipe_right"
    SWIPE_UP = "swipe_up"
    SWIPE_DOWN = "swipe_down"
    PINCH = "pinch"
    OPEN_PALM = "open_palm"
    FIST = "fist"


@dataclass(frozen=True)
class GestureEvent:
    """A provider-neutral gesture observation."""

    kind: GestureKind
    confidence: float = 1.0
    source: str = "unknown"
    timestamp: float = field(default_factory=monotonic)
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class GestureAction:
    """Safe logical action produced from a gesture."""

    name: str
    payload: Mapping[str, str] = field(default_factory=dict)
