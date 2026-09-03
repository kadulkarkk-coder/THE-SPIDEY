"""Ambiguity detection and safe clarification support."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AmbiguityReport:
    ambiguous: bool
    reasons: tuple[str, ...]
    candidates: tuple[str, ...]


class AmbiguityResolver:
    """Detects underspecified requests; it never invents missing user intent."""

    def inspect(self, text: str, candidates: tuple[str, ...] = ()) -> AmbiguityReport:
        cleaned = " ".join(text.split())
        reasons: list[str] = []
        if not cleaned:
            reasons.append("empty request")
        if len(cleaned.split()) <= 2 and cleaned.lower() in {"do it", "fix it", "open it", "that one"}:
            reasons.append("missing referent")
        if candidates and len(candidates) > 1:
            reasons.append("multiple plausible interpretations")
        return AmbiguityReport(bool(reasons), tuple(reasons), tuple(candidates))

    @staticmethod
    def clarification(report: AmbiguityReport) -> str:
        if not report.ambiguous:
            return "No clarification needed."
        if report.candidates:
            return "Please choose one: " + ", ".join(report.candidates)
        return "Please provide a little more detail so WEBSTER can act safely."
