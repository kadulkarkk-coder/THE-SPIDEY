"""In-memory clipboard boundary with explicit read/write authorization."""
from __future__ import annotations
from threading import RLock

class Clipboard:
    def __init__(self) -> None: self._text = ""; self._lock = RLock()
    def read(self, *, authorized: bool = False) -> str:
        if not authorized: raise PermissionError("clipboard read requires explicit authorization")
        with self._lock: return self._text
    def write(self, text: str, *, authorized: bool = False) -> None:
        if not authorized: raise PermissionError("clipboard write requires explicit authorization")
        if "\x00" in text: raise ValueError("clipboard text contains an invalid character")
        with self._lock: self._text = text
    def clear(self, *, authorized: bool = False) -> None: self.write("", authorized=authorized)
