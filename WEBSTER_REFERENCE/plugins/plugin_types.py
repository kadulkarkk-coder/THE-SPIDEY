"""Core contracts for safe, lightweight WEBSTER plugins."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class PluginStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    ERROR = "error"


@dataclass(frozen=True)
class PluginSpec:
    plugin_id: str
    name: str
    description: str
    capabilities: tuple[str, ...] = ()
    builtin: bool = False
    requires_network: bool = False
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.plugin_id.strip() or not self.name.strip():
            raise ValueError("plugin_id and name must not be empty")
        if any(not capability.strip() for capability in self.capabilities):
            raise ValueError("plugin capabilities must not be empty")


@dataclass(frozen=True)
class PluginState:
    plugin_id: str
    status: PluginStatus
    message: str = ""
