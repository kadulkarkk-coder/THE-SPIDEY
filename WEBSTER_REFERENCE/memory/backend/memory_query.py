"""Structured memory query model."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class MemoryQuery:
    text: str
    kind: str | None = None
    limit: int = 10

    def normalized(self) -> "MemoryQuery":
        return MemoryQuery(" ".join(self.text.split()), self.kind.strip().lower() if self.kind else None, max(1, self.limit))
