"""B4 real Windows window discovery and safe focus/state control."""
from __future__ import annotations

from dataclasses import dataclass
import ctypes
import os


@dataclass(frozen=True)
class WindowInfo:
    handle: int
    title: str
    visible: bool
    minimized: bool
    maximized: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "handle": self.handle,
            "title": self.title,
            "visible": self.visible,
            "minimized": self.minimized,
            "maximized": self.maximized,
        }


class WindowController:
    SW_MINIMIZE = 6
    SW_MAXIMIZE = 3
    SW_RESTORE = 9

    def __init__(self) -> None:
        self._user32 = ctypes.windll.user32 if os.name == "nt" else None

    def _require_windows(self) -> None:
        if self._user32 is None:
            raise OSError("Window control is currently implemented for Windows.")

    def list(self, query: str = "", limit: int = 50) -> tuple[WindowInfo, ...]:
        self._require_windows()
        user32 = self._user32
        rows: list[WindowInfo] = []
        callback_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

        def callback(hwnd, _lparam):
            if not user32.IsWindowVisible(hwnd):
                return True
            length = user32.GetWindowTextLengthW(hwnd)
            if length <= 0:
                return True
            buffer = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buffer, length + 1)
            title = buffer.value.strip()
            if not title:
                return True
            if query and query.casefold() not in title.casefold():
                return True
            placement = ctypes.create_int_buffer(44)
            minimized = bool(user32.IsIconic(hwnd))
            maximized = bool(user32.IsZoomed(hwnd))
            rows.append(WindowInfo(int(hwnd), title, True, minimized, maximized))
            return len(rows) < limit

        user32.EnumWindows(callback_type(callback), 0)
        return tuple(rows[:limit])

    def focus(self, handle: int) -> str:
        self._require_windows()
        if handle <= 0 or not self._user32.IsWindow(handle):
            raise ValueError("Unknown window handle.")
        self._user32.ShowWindow(handle, self.SW_RESTORE)
        if not self._user32.SetForegroundWindow(handle):
            raise RuntimeError("Windows rejected the focus request.")
        return f"Focused window {handle}"

    def minimize(self, handle: int) -> str:
        self._require_windows()
        if handle <= 0 or not self._user32.IsWindow(handle):
            raise ValueError("Unknown window handle.")
        self._user32.ShowWindow(handle, self.SW_MINIMIZE)
        return f"Minimized window {handle}"

    def maximize(self, handle: int) -> str:
        self._require_windows()
        if handle <= 0 or not self._user32.IsWindow(handle):
            raise ValueError("Unknown window handle.")
        self._user32.ShowWindow(handle, self.SW_MAXIMIZE)
        return f"Maximized window {handle}"

    def restore(self, handle: int) -> str:
        self._require_windows()
        if handle <= 0 or not self._user32.IsWindow(handle):
            raise ValueError("Unknown window handle.")
        self._user32.ShowWindow(handle, self.SW_RESTORE)
        return f"Restored window {handle}"
