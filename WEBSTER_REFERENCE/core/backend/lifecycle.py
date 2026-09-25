"""WEBSTER application lifecycle management."""

from __future__ import annotations

from enum import Enum
from threading import RLock


class LifecycleState(str, Enum):
    CREATED = "created"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"


class LifecycleManager:
    """Small deterministic state machine for application startup/shutdown."""

    def __init__(self) -> None:
        self._state = LifecycleState.CREATED
        self._lock = RLock()

    @property
    def state(self) -> LifecycleState:
        with self._lock:
            return self._state

    def start(self) -> None:
        with self._lock:
            if self._state is LifecycleState.RUNNING:
                return
            if self._state not in (LifecycleState.CREATED, LifecycleState.STOPPED):
                raise RuntimeError(f"Cannot start from state: {self._state.value}")
            self._state = LifecycleState.STARTING
            self._state = LifecycleState.RUNNING

    def stop(self) -> None:
        with self._lock:
            if self._state in (LifecycleState.STOPPED, LifecycleState.CREATED):
                self._state = LifecycleState.STOPPED
                return
            if self._state is not LifecycleState.RUNNING:
                raise RuntimeError(f"Cannot stop from state: {self._state.value}")
            self._state = LifecycleState.STOPPING
            self._state = LifecycleState.STOPPED

    def fail(self) -> None:
        with self._lock:
            self._state = LifecycleState.FAILED
