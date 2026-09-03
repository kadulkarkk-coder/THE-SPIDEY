"""Portable window-state registry for controlled desktop orchestration."""
from __future__ import annotations
from dataclasses import dataclass
from threading import RLock

@dataclass(frozen=True)
class WindowState:
    window_id: str
    title: str
    state: str = "normal"

class WindowManager:
    VALID_STATES = frozenset({"normal", "minimized", "maximized", "closed"})
    def __init__(self) -> None: self._windows: dict[str, WindowState] = {}; self._lock = RLock()
    def register(self, window_id: str, title: str) -> WindowState:
        wid, name = window_id.strip(), title.strip()
        if not wid: raise ValueError("window_id is required")
        item = WindowState(wid, name)
        with self._lock: self._windows[wid] = item
        return item
    def set_state(self, window_id: str, state: str) -> WindowState:
        state = state.strip().lower()
        if state not in self.VALID_STATES: raise ValueError("invalid window state")
        with self._lock:
            current = self._windows[window_id.strip()]
            item = WindowState(current.window_id, current.title, state); self._windows[current.window_id] = item; return item
    def list(self) -> tuple[WindowState, ...]:
        with self._lock: return tuple(self._windows.values())
