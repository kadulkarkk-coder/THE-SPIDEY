"""Typed request/response contracts for WEBSTER commands."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class CommandRequest:
    """Normalized command request entering the runtime."""

    text: str
    request_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "CommandRequest":
        return CommandRequest(
            text=self.text.strip(),
            request_id=self.request_id,
            created_at=self.created_at,
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class CommandResponse:
    """Stable response returned by command processing."""

    request_id: str
    ok: bool
    message: str
    data: dict[str, Any] = field(default_factory=dict)
    error_code: str | None = None

    @classmethod
    def success(cls, request: CommandRequest, message: str, data: dict[str, Any] | None = None) -> "CommandResponse":
        return cls(request.request_id, True, message, data or {})

    @classmethod
    def failure(cls, request: CommandRequest, message: str, error_code: str) -> "CommandResponse":
        return cls(request.request_id, False, message, {}, error_code)
