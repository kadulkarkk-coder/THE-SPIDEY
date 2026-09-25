"""B5 real Windows keyboard driver using the Win32 SendInput API."""
from __future__ import annotations

import ctypes
import os
import time


class KeyboardDriver:
    """Injects only explicitly requested keyboard actions; no key listener is installed."""

    _KEYS = {
        "backspace": 0x08, "tab": 0x09, "enter": 0x0D, "shift": 0x10,
        "ctrl": 0x11, "alt": 0x12, "esc": 0x1B, "space": 0x20,
        "left": 0x25, "up": 0x26, "right": 0x27, "down": 0x28,
        "delete": 0x2E, "home": 0x24, "end": 0x23,
    }
    _KEYS.update({f"f{i}": 0x6F + i for i in range(1, 13)})

    def __init__(self) -> None:
        self._user32 = ctypes.windll.user32 if os.name == "nt" else None

    def _require_windows(self) -> None:
        if self._user32 is None:
            raise OSError("Keyboard injection is currently implemented for Windows.")

    def _vk(self, key: str) -> int:
        value = key.strip().casefold()
        if value in self._KEYS:
            return self._KEYS[value]
        if len(value) == 1 and value.isascii():
            return ord(value.upper())
        raise ValueError(f"Unsupported keyboard key: {key}")

    def press(self, key: str, modifiers: tuple[str, ...] = ()) -> str:
        self._require_windows()
        key_code = self._vk(key)
        modifier_codes = [self._vk(item) for item in modifiers]
        inputs = []

        class KEYBDINPUT(ctypes.Structure):
            _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort),
                        ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong),
                        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

        class INPUT(ctypes.Structure):
            _fields_ = [("type", ctypes.c_ulong), ("ki", KEYBDINPUT)]

        for code in [*modifier_codes, key_code]:
            inputs.append(INPUT(1, KEYBDINPUT(code, 0, 0, 0, None)))
        for code in [key_code, *reversed(modifier_codes)]:
            inputs.append(INPUT(1, KEYBDINPUT(code, 0, 2, 0, None)))

        array = (INPUT * len(inputs))(*inputs)
        sent = self._user32.SendInput(len(inputs), ctypes.byref(array), ctypes.sizeof(INPUT))
        if sent != len(inputs):
            raise RuntimeError("Windows rejected the keyboard input.")
        return "Pressed " + "+".join((*modifiers, key))

    def type_text(self, text: str) -> str:
        self._require_windows()
        value = text.replace("\r", " ").replace("\n", " ")
        if not value:
            return "Nothing to type."
        if len(value) > 500:
            raise ValueError("Typed text is limited to 500 characters per action.")
        for char in value:
            if char.isascii() and char.isprintable():
                self.press(char)
            elif char == " ":
                self.press("space")
            else:
                raise ValueError("Only basic printable ASCII text is supported by this keyboard driver.")
            time.sleep(0.003)
        return f"Typed {len(value)} characters"
