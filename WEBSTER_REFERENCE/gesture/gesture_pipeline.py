"""Low-overhead gesture pipeline for the desktop WEBSTER build."""
from __future__ import annotations

from dataclasses import dataclass

from .gesture_detector import GestureDetector
from .gesture_mapper import GestureMapper
from .gesture_permissions import GesturePermissions
from .gesture_types import GestureAction, GestureEvent


@dataclass(frozen=True)
class GestureResult:
    """Outcome of processing one gesture observation."""

    event: GestureEvent
    action: GestureAction | None


class GesturePipeline:
    """Process one event at a time; never owns a camera or polling loop."""

    def __init__(self, *, permissions: GesturePermissions | None = None,
                 detector: GestureDetector | None = None,
                 mapper: GestureMapper | None = None) -> None:
        self.permissions = permissions or GesturePermissions()
        self.detector = detector or GestureDetector()
        self.mapper = mapper or GestureMapper()

    def process(self, principal: str, kind: str, *, confidence: float = 1.0,
                source: str = "provider") -> GestureResult | None:
        if not self.permissions.allowed(principal, "gesture_control"):
            raise PermissionError("gesture capability is not permitted")
        event = self.detector.detect(kind, confidence=confidence, source=source)
        if event is None:
            return None
        return GestureResult(event=event, action=self.mapper.map(event.kind))
