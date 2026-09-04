"""Coordinate Floating Orb state transitions without owning a UI toolkit."""
from __future__ import annotations

from .orb_state import OrbStateStore
from .orb_types import OrbAction, OrbEvent, OrbState


class OrbController:
    """Translate WEBSTER lifecycle signals into lightweight Orb state."""

    def __init__(self, state: OrbStateStore | None = None) -> None:
        self.state = state or OrbStateStore()

    def set_state(self, state: OrbState, message: str = "") -> OrbEvent:
        return self.state.set(state, message)

    def hide(self) -> OrbEvent:
        return self.set_state(OrbState.HIDDEN)

    def idle(self, message: str = "Ready") -> OrbEvent:
        return self.set_state(OrbState.IDLE, message)

    def listening(self) -> OrbEvent:
        return self.set_state(OrbState.LISTENING, "Listening")

    def thinking(self, message: str = "Thinking") -> OrbEvent:
        return self.set_state(OrbState.THINKING, message)

    def acting(self, message: str = "Working") -> OrbEvent:
        return self.set_state(OrbState.ACTING, message)

    def error(self, message: str) -> OrbEvent:
        return self.set_state(OrbState.ERROR, message)

    def handle(self, action: OrbAction) -> OrbEvent:
        mapping = {
            "hide": OrbState.HIDDEN,
            "idle": OrbState.IDLE,
            "listen": OrbState.LISTENING,
            "think": OrbState.THINKING,
            "act": OrbState.ACTING,
            "error": OrbState.ERROR,
        }
        state = mapping.get(action.name.strip().lower())
        if state is None:
            raise ValueError(f"unsupported orb action: {action.name}")
        return self.set_state(state, action.value)
