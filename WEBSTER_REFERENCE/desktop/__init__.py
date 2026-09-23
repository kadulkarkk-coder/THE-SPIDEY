"""WEBSTER real desktop/system capabilities."""

from .desktop_runtime import DesktopAction, DesktopRuntime
from .system_interface import SystemInterface, SystemSnapshot
from .process_discovery import ProcessDiscovery, ProcessMatch
from .window_control import WindowController, WindowInfo
from .keyboard_driver import KeyboardDriver

__all__ = [
    "DesktopAction", "DesktopRuntime",
    "SystemInterface", "SystemSnapshot",
    "ProcessDiscovery", "ProcessMatch",
    "WindowController", "WindowInfo",
    "KeyboardDriver",
]
