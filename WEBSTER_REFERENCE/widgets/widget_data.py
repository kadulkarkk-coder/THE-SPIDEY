"""Small, provider-neutral data contracts for WEBSTER desktop widgets."""
from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Mapping


@dataclass(frozen=True)
class WidgetData:
    """Serializable widget payload with a timestamp and optional metadata."""

    values: Mapping[str, object] = field(default_factory=dict)
    timestamp: float = field(default_factory=time)
    source: str = "local"


class WidgetDataError(ValueError):
    """Raised when widget data cannot be accepted."""
