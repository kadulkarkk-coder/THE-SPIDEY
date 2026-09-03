"""Deterministic conditions for workflow branching."""
from __future__ import annotations
from typing import Any, Callable

class ConditionEngine:
    def evaluate(self, value: Any, predicate: Callable[[Any], bool]) -> bool:
        if not callable(predicate): raise TypeError("predicate must be callable")
        try: return bool(predicate(value))
        except Exception: return False
