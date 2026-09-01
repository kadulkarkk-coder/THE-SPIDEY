"""WEBSTER synchronous in-process event bus.

Sprint 1 implementation: small, dependency-free, thread-safe pub/sub primitive.
"""

from __future__ import annotations

from collections import defaultdict
from threading import RLock
from typing import Any, Callable

EventHandler = Callable[[Any], None]


class EventBus:
    """Publish named events to registered handlers."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
        self._lock = RLock()

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        if not event_name.strip():
            raise ValueError("event_name must not be empty")
        with self._lock:
            if handler not in self._handlers[event_name]:
                self._handlers[event_name].append(handler)

    def unsubscribe(self, event_name: str, handler: EventHandler) -> None:
        with self._lock:
            handlers = self._handlers.get(event_name, [])
            if handler in handlers:
                handlers.remove(handler)
            if not handlers:
                self._handlers.pop(event_name, None)

    def publish(self, event_name: str, payload: Any = None) -> int:
        """Publish an event and return the number of handlers invoked."""
        with self._lock:
            handlers = tuple(self._handlers.get(event_name, ()))
        for handler in handlers:
            handler(payload)
        return len(handlers)

    def clear(self) -> None:
        with self._lock:
            self._handlers.clear()

    def handler_count(self, event_name: str | None = None) -> int:
        with self._lock:
            if event_name is not None:
                return len(self._handlers.get(event_name, ()))
            return sum(len(items) for items in self._handlers.values())
