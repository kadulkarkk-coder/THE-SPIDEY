"""User-configurable voice settings with safe defaults."""
from __future__ import annotations
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class VoiceSettings:
    enabled: bool = True
    language: str = "en-IN"
    input_device: str | None = None
    output_device: str | None = None
    speech_rate: int = 175
    volume: float = 1.0

    def normalized(self) -> "VoiceSettings":
        language = self.language.strip() or "en-IN"
        return replace(
            self,
            language=language,
            speech_rate=max(50, min(300, int(self.speech_rate))),
            volume=max(0.0, min(1.0, float(self.volume))),
        )

class VoiceSettingsStore:
    def __init__(self, settings: VoiceSettings | None = None) -> None:
        self._settings = (settings or VoiceSettings()).normalized()

    def get(self) -> VoiceSettings:
        return self._settings

    def update(self, **changes: object) -> VoiceSettings:
        self._settings = replace(self._settings, **changes).normalized()
        return self._settings
