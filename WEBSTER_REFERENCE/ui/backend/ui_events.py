"""Structured UI events for connecting presentation actions to WEBSTER runtime."""
from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Mapping


@dataclass(frozen=True)
class UIActionEvent:
    """A user-facing action emitted by the UI layer."""

    name: str
    source: str = "ui"
    payload: Mapping[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("event name must not be empty")
        if not self.source.strip():
            raise ValueError("event source must not be empty")


class UIEventBus:
    """Small synchronous event bus; handlers are invoked in registration order."""

    def __init__(self) -> None:
        self._handlers: dict[str, list] = {}

    def subscribe(self, name: str, handler) -> None:
        key = name.strip()
        if not key:
            raise ValueError("event name must not be empty")
        self._handlers.setdefault(key, []).append(handler)

    def emit(self, event: UIActionEvent) -> None:
        for handler in tuple(self._handlers.get(event.name, ())):
            handler(event)
