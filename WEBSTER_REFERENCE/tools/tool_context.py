"""Explicit context passed to tool execution without global state."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ToolContext:
    request_id: str = ""
    actor: str = "webster"
    values: dict[str, Any] = field(default_factory=dict)
    dry_run: bool = False

    def with_value(self, key: str, value: Any) -> "ToolContext":
        updated = dict(self.values)
        updated[key.strip()] = value
        return ToolContext(self.request_id, self.actor, updated, self.dry_run)
