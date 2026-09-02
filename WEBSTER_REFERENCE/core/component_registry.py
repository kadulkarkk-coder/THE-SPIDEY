"""WEBSTER component registry.

Keeps runtime components discoverable without coupling the application to concrete
implementations. Registration is explicit and duplicate names are rejected.
"""
from __future__ import annotations
from dataclasses import dataclass
from threading import RLock
from typing import Any, Callable

@dataclass(frozen=True)
class ComponentRecord:
    name: str
    component: Any
    description: str = ""

class ComponentRegistry:
    def __init__(self) -> None:
        self._items: dict[str, ComponentRecord] = {}
        self._lock = RLock()

    def register(self, name: str, component: Any, description: str = "") -> ComponentRecord:
        name = name.strip().lower()
        if not name:
            raise ValueError("Component name cannot be empty")
        with self._lock:
            if name in self._items:
                raise ValueError(f"Component already registered: {name}")
            record = ComponentRecord(name, component, description)
            self._items[name] = record
            return record

    def get(self, name: str) -> Any | None:
        with self._lock:
            record = self._items.get(name.strip().lower())
            return record.component if record else None

    def records(self) -> tuple[ComponentRecord, ...]:
        with self._lock:
            return tuple(self._items.values())

    def names(self) -> tuple[str, ...]:
        return tuple(record.name for record in self.records())

    def unregister(self, name: str) -> bool:
        with self._lock:
            return self._items.pop(name.strip().lower(), None) is not None

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
