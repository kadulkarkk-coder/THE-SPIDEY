"""Bounded fallback selection for failed or unavailable tools."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class ToolFallback:
    name: str
    handler: Callable[[Any], Any]

class ToolFallbackChain:
    def __init__(self, fallbacks: tuple[ToolFallback, ...] = ()) -> None:
        self.fallbacks = fallbacks

    def add(self, fallback: ToolFallback) -> None:
        if not fallback.name.strip(): raise ValueError("fallback name is required")
        self.fallbacks += (fallback,)

    def run(self, value: Any = None):
        errors = []
        for fallback in self.fallbacks:
            try:
                return fallback.handler(value), fallback.name
            except Exception as exc:
                errors.append(f"{fallback.name}: {exc}")
        return None, "; ".join(errors)
