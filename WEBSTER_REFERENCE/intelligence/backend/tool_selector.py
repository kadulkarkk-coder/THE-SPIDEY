"""Capability-aware tool selection boundary."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ToolCandidate:
    name: str
    capability: str
    score: float


class ToolSelector:
    """Ranks declared tools; selection never executes a tool."""

    def rank(self, capability: str, tools: tuple[ToolCandidate, ...]) -> tuple[ToolCandidate, ...]:
        capability = capability.strip().lower()
        matches = [tool for tool in tools if tool.capability.lower() == capability]
        return tuple(sorted(matches, key=lambda tool: tool.score, reverse=True))

    @staticmethod
    def best(candidates: tuple[ToolCandidate, ...]) -> ToolCandidate | None:
        return max(candidates, key=lambda item: item.score, default=None)
