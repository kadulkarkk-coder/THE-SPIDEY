"""Provider-neutral gesture detection boundary.

The reference implementation intentionally does not start a camera or spawn a
continuous vision loop. A future platform adapter can feed observations into
``detect`` while the phone build can omit this module entirely.
"""
from __future__ import annotations

from dataclasses import dataclass

from .gesture_types import GestureEvent, GestureKind


@dataclass(frozen=True)
class GestureThresholds:
    """Tunable thresholds kept in data so providers remain replaceable."""

    minimum_confidence: float = 0.70

    def __post_init__(self) -> None:
        if not 0.0 <= self.minimum_confidence <= 1.0:
            raise ValueError("minimum_confidence must be between 0 and 1")


class GestureDetector:
    """Normalize provider observations without owning hardware resources."""

    def __init__(self, thresholds: GestureThresholds | None = None) -> None:
        self.thresholds = thresholds or GestureThresholds()

    def detect(self, kind: GestureKind | str, *, confidence: float = 1.0,
               source: str = "provider") -> GestureEvent | None:
        normalized = kind if isinstance(kind, GestureKind) else GestureKind(str(kind).strip().lower())
        if confidence < self.thresholds.minimum_confidence:
            return None
        return GestureEvent(kind=normalized, confidence=confidence, source=source)
