"""Normalized, inspectable result contract for tool execution."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class ToolResult:
    tool: str
    ok: bool
    value: Any = None
    error: str | None = None
    code: str = ""
    request_id: str = ""

    @classmethod
    def success(cls, tool: str, value: Any = None, *, request_id: str = "") -> "ToolResult":
        return cls(tool.strip().lower(), True, value=value, request_id=request_id)

    @classmethod
    def failure(cls, tool: str, error: str, *, code: str = "ERROR", request_id: str = "") -> "ToolResult":
        return cls(tool.strip().lower(), False, error=str(error), code=code, request_id=request_id)
