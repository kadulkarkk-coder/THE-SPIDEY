"""Wake interaction state machine for voice sessions."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class WakeState:
    active: bool = False
    turns: int = 0

class WakeInteraction:
    def __init__(self) -> None:
        self._state = WakeState()

    @property
    def state(self) -> WakeState:
        return self._state

    def wake(self) -> WakeState:
        self._state = WakeState(True, self._state.turns)
        return self._state

    def consume_turn(self) -> WakeState:
        if self._state.active:
            self._state = WakeState(True, self._state.turns + 1)
        return self._state

    def sleep(self) -> WakeState:
        self._state = WakeState(False, self._state.turns)
        return self._state
