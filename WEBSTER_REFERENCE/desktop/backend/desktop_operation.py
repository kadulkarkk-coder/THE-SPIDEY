"""Structured desktop operation definitions without executing OS input."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class DesktopOperation:
    capability: str
    target: str = ""
    parameters: tuple[tuple[str, str], ...] = ()

    def normalized(self) -> "DesktopOperation":
        capability = self.capability.strip().lower()
        target = self.target.strip()
        if not capability:
            raise ValueError("capability is required")
        return DesktopOperation(capability, target, tuple((str(k), str(v)) for k, v in self.parameters))
