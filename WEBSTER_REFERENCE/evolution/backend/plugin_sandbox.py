"""Lightweight, bounded sandbox contract for testing evolved plugins."""
from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Callable


@dataclass(frozen=True)
class SandboxResult:
    passed: bool
    duration_ms: float
    message: str = ""


class PluginSandbox:
    """Runs supplied validation callbacks with a time budget.

    The sandbox deliberately does not execute arbitrary source code itself.
    A platform-specific isolated runner can be attached later.
    """

    def run(self, check: Callable[[], None], *, timeout_ms: float = 1000.0) -> SandboxResult:
        if timeout_ms <= 0:
            raise ValueError("timeout_ms must be positive")
        started = monotonic()
        try:
            check()
            duration = (monotonic() - started) * 1000.0
            if duration > timeout_ms:
                return SandboxResult(False, duration, "sandbox time budget exceeded")
            return SandboxResult(True, duration, "sandbox checks passed")
        except Exception as exc:
            duration = (monotonic() - started) * 1000.0
            return SandboxResult(False, duration, str(exc))
