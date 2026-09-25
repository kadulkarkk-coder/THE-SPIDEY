"""Standard contract for safe, observable WEBSTER tools."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str = ""
    capabilities: frozenset[str] = frozenset()
    risk: str = "low"
    requires_confirmation: bool = False
    parameters: tuple[str, ...] = ()

    def normalized_name(self) -> str:
        return self.name.strip().lower()

@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    request_id: str = ""

@dataclass(frozen=True)
class ToolBinding:
    spec: ToolSpec
    handler: Callable[..., Any]
