"""High-level voice orchestration boundary for WEBSTER."""
from __future__ import annotations
from dataclasses import dataclass
from .speech_to_text import SpeechToText, SpeechInput
from .text_to_speech import TextToSpeech, SpeechOutput
from .voice_settings import VoiceSettingsStore

@dataclass(frozen=True)
class VoiceTurn:
    input: SpeechInput
    output: SpeechOutput | None = None

class VoiceController:
    def __init__(self, speech_to_text: SpeechToText | None = None, text_to_speech: TextToSpeech | None = None, settings: VoiceSettingsStore | None = None) -> None:
        self.stt = speech_to_text or SpeechToText()
        self.tts = text_to_speech or TextToSpeech()
        self.settings = settings or VoiceSettingsStore()

    def transcribe(self, audio: object) -> SpeechInput:
        if not self.settings.get().enabled:
            return SpeechInput("", 0.0, "disabled")
        return self.stt.transcribe(audio)

    def respond(self, text: str) -> SpeechOutput | None:
        if not self.settings.get().enabled:
            return None
        return self.tts.speak(text)

    def process(self, audio: object, response_text: str | None = None) -> VoiceTurn:
        captured = self.transcribe(audio)
        output = self.respond(response_text) if response_text is not None and captured.text else None
        return VoiceTurn(captured, output)
