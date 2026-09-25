"""Confidence calibration utilities for WEBSTER."""
from __future__ import annotations

class ConfidenceCalibrator:
    def calibrate(self, confidence: float, *, evidence_quality: float = 1.0) -> float:
        confidence = max(0.0, min(1.0, confidence))
        evidence_quality = max(0.0, min(1.0, evidence_quality))
        return round(confidence * (0.5 + 0.5 * evidence_quality), 4)

    def band(self, confidence: float) -> str:
        value = max(0.0, min(1.0, confidence))
        if value >= 0.8:
            return "high"
        if value >= 0.5:
            return "medium"
        return "low"
