"""Lightweight metrics for voice interaction."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class VoiceMetrics:
    started: int = 0
    transcribed: int = 0
    spoken: int = 0
    interrupted: int = 0
    failed: int = 0

class VoiceMetricsCollector:
    def collect(self, events) -> VoiceMetrics:
        counts = {"started": 0, "transcribed": 0, "spoken": 0, "interrupted": 0, "failed": 0}
        for event in events:
            name = getattr(event, "event", "")
            if name in counts:
                counts[name] += 1
        return VoiceMetrics(**counts)
