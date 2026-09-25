"""Command-center presentation model for WEBSTER runtime status."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandStatus:
    state: str
    message: str = ""
    progress: float | None = None

    def __post_init__(self) -> None:
        if not self.state.strip():
            raise ValueError("state must not be empty")
        if self.progress is not None and not 0.0 <= self.progress <= 1.0:
            raise ValueError("progress must be between 0 and 1")


class CommandCenter:
    """Hold the latest runtime command status for a future renderer."""

    def __init__(self) -> None:
        self._status = CommandStatus("idle", "Ready", 0.0)

    def update(self, state: str, message: str = "", progress: float | None = None) -> CommandStatus:
        self._status = CommandStatus(state, message, progress)
        return self._status

    def snapshot(self) -> CommandStatus:
        return self._status
