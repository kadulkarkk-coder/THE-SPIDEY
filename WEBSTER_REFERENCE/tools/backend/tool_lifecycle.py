"""Lifecycle management for registered WEBSTER tools."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class ToolLifecycleState:
    tool: str
    state: str
    changed_at: datetime

class ToolLifecycle:
    """Track tool availability without executing the tool."""
    VALID = frozenset({"registered", "ready", "paused", "disabled"})
    def __init__(self) -> None:
        self._states: dict[str, ToolLifecycleState] = {}

    def set_state(self, tool: str, state: str) -> ToolLifecycleState:
        name, value = tool.strip().lower(), state.strip().lower()
        if not name: raise ValueError("tool name is required")
        if value not in self.VALID: raise ValueError(f"invalid lifecycle state: {value}")
        item = ToolLifecycleState(name, value, datetime.now(timezone.utc))
        self._states[name] = item
        return item

    def get_state(self, tool: str) -> ToolLifecycleState:
        name = tool.strip().lower()
        return self._states.get(name, ToolLifecycleState(name, "registered", datetime.now(timezone.utc)))

    def usable(self, tool: str) -> bool:
        return self.get_state(tool).state == "ready"
