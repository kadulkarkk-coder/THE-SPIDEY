"""Replaceable speech-recognition provider boundary with an offline-safe adapter."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class SpeechInput:
    text: str
    confidence: float = 0.0
    provider: str = "offline"

class SpeechRecognizer(Protocol):
    name: str
    def recognize(self, audio: object) -> SpeechInput: ...

class OfflineSpeechRecognizer:
    name = "offline"

    def recognize(self, audio: object) -> SpeechInput:
        if isinstance(audio, str):
            text = " ".join(audio.split())
            return SpeechInput(text, 1.0 if text else 0.0, self.name)
        return SpeechInput("", 0.0, self.name)

class SpeechToText:
    def __init__(self, recognizer: SpeechRecognizer | None = None) -> None:
        self.recognizer = recognizer or OfflineSpeechRecognizer()

    def transcribe(self, audio: object) -> SpeechInput:
        return self.recognizer.recognize(audio)
