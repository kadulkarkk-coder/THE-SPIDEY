"""Controlled voice interaction pipeline."""
from __future__ import annotations
from .voice_controller import VoiceController, VoiceTurn
from .wake_interaction import WakeInteraction
from .interrupt_handler import InterruptHandler
from .voice_events import VoiceEventLog

class VoicePipeline:
    def __init__(self, controller: VoiceController | None = None) -> None:
        self.controller = controller or VoiceController()
        self.wake = WakeInteraction()
        self.interrupts = InterruptHandler()
        self.events = VoiceEventLog()

    def start(self) -> None:
        self.wake.wake()
        self.events.emit("started")

    def interrupt(self) -> None:
        self.interrupts.request()
        self.events.emit("interrupted")

    def process(self, audio: object, response_text: str | None = None) -> VoiceTurn:
        if not self.wake.state.active:
            raise RuntimeError("voice interaction is not active")
        if self.interrupts.consume():
            return VoiceTurn(self.controller.transcribe(None), None)
        turn = self.controller.process(audio, response_text)
        if turn.input.text:
            self.wake.consume_turn()
            self.events.emit("transcribed", turn.input.text)
        if turn.output is not None:
            self.events.emit("spoken")
        return turn

    def stop(self) -> None:
        self.wake.sleep()
