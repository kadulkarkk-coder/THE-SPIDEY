"""Validate safe Floating Orb state transitions."""
from __future__ import annotations

from .orb_types import OrbState


class OrbTransitionPolicy:
    """Keep state transitions predictable and presentation-focused."""

    ALLOWED = {
        OrbState.HIDDEN: {OrbState.IDLE},
        OrbState.IDLE: {OrbState.HIDDEN, OrbState.LISTENING, OrbState.THINKING, OrbState.ERROR},
        OrbState.LISTENING: {OrbState.IDLE, OrbState.THINKING, OrbState.ERROR},
        OrbState.THINKING: {OrbState.ACTING, OrbState.IDLE, OrbState.ERROR},
        OrbState.ACTING: {OrbState.IDLE, OrbState.THINKING, OrbState.ERROR},
        OrbState.ERROR: {OrbState.IDLE, OrbState.HIDDEN},
    }

    def allowed(self, current: OrbState, target: OrbState) -> bool:
        return target in self.ALLOWED.get(current, set())
