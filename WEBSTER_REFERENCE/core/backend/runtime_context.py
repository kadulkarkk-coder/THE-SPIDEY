"""Shared runtime context passed between WEBSTER core components."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

@dataclass
class RuntimeContext:
    session_id: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    values: dict[str, Any] = field(default_factory=dict)

    def set(self, key: str, value: Any) -> None:
        self.values[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.values.get(key, default)

    def snapshot(self) -> dict[str, Any]:
        return {"session_id": self.session_id, "created_at": self.created_at.isoformat(), "values": dict(self.values)}
