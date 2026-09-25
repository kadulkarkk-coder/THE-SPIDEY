"""Replaceable speech-synthesis provider boundary without hard dependencies."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class SpeechOutput:
    text: str
    provider: str = "silent"
    spoken: bool = False

class SpeechSynthesizer(Protocol):
    name: str
    def synthesize(self, text: str) -> SpeechOutput: ...

class SilentSynthesizer:
    name = "silent"
    def synthesize(self, text: str) -> SpeechOutput:
        return SpeechOutput(" ".join(text.split()), self.name, False)

class TextToSpeech:
    def __init__(self, synthesizer: SpeechSynthesizer | None = None) -> None:
        self.synthesizer = synthesizer or SilentSynthesizer()

    def speak(self, text: str) -> SpeechOutput:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return self.synthesizer.synthesize(text)
