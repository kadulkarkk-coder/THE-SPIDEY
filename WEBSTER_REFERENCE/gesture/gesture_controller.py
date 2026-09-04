"""Orchestrate safe gesture processing without owning hardware loops."""
from __future__ import annotations

from .gesture_metrics import GestureMetrics
from .gesture_observer import GestureObserver
from .gesture_permissions import GesturePermissions
from .gesture_pipeline import GesturePipeline, GestureResult


class GestureController:
    """Coordinate gesture input, policy, observation, and metrics."""

    def __init__(self, *, permissions: GesturePermissions | None = None,
                 pipeline: GesturePipeline | None = None,
                 observer: GestureObserver | None = None,
                 metrics: GestureMetrics | None = None) -> None:
        self.permissions = permissions or GesturePermissions()
        self.pipeline = pipeline or GesturePipeline(permissions=self.permissions)
        self.observer = observer or GestureObserver()
        self.metrics = metrics or GestureMetrics()

    def process(self, principal: str, kind: str, *, confidence: float = 1.0,
                source: str = "provider") -> GestureResult | None:
        try:
            result = self.pipeline.process(principal, kind, confidence=confidence, source=source)
            accepted = result is not None and result.action is not None
            self.metrics.record(accepted)
            self.observer.record("process", kind, accepted, "mapped" if accepted else "ignored")
            return result
        except Exception as exc:
            self.metrics.record(False)
            self.observer.record("process", kind, False, str(exc))
            raise
