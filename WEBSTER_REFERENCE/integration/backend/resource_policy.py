"""Resource-conscious defaults for WEBSTER clients."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResourcePolicy:
    """Keep the always-on core lightweight on laptop and phone hardware."""

    background_polling: bool = False
    camera_continuous_mode: bool = False
    max_worker_threads: int = 4
    idle_timeout_seconds: int = 300
    prefer_local_cached_results: bool = True

    def validate(self) -> None:
        if self.max_worker_threads < 1:
            raise ValueError("max_worker_threads must be positive")
        if self.idle_timeout_seconds < 0:
            raise ValueError("idle_timeout_seconds cannot be negative")
