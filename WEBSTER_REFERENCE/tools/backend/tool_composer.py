"""Compose small tools into an explicit sequential workflow."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class ToolStep:
    name: str
    handler: Callable[[Any], Any]

class ToolComposer:
    def __init__(self, steps: tuple[ToolStep, ...] = ()) -> None:
        self.steps = steps

    def compose(self, *steps: ToolStep) -> "ToolComposer":
        if any(not step.name.strip() for step in steps): raise ValueError("tool step names are required")
        return ToolComposer(self.steps + steps)

    def run(self, value: Any = None) -> Any:
        current = value
        for step in self.steps:
            current = step.handler(current)
        return current
