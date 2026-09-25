"""Deterministic trigger definitions for automation workflows."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class Trigger:
    name: str
    predicate: Callable[[Any], bool]

class TriggerRegistry:
    def __init__(self) -> None: self._triggers: dict[str, Trigger] = {}
    def register(self, trigger: Trigger) -> None:
        if not trigger.name.strip(): raise ValueError("trigger name is required")
        self._triggers[trigger.name.strip().lower()] = trigger
    def fired(self, event: Any) -> tuple[Trigger, ...]:
        result = []
        for trigger in self._triggers.values():
            try:
                if trigger.predicate(event): result.append(trigger)
            except Exception: continue
        return tuple(result)
    def names(self) -> tuple[str, ...]: return tuple(sorted(self._triggers))
