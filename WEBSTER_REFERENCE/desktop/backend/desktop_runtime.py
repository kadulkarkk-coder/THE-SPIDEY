"""B1-B5 functional desktop runtime for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass
import re
import shlex
import subprocess
import os
import webbrowser

from .system_interface import SystemInterface
from .process_discovery import ProcessDiscovery
from .application_launcher import ApplicationLauncher
from .window_control import WindowController
from .keyboard_driver import KeyboardDriver


@dataclass(frozen=True)
class DesktopAction:
    handled: bool
    ok: bool
    message: str
    capability: str = ""
    data: dict[str, object] | None = None


class DesktopRuntime:
    """Natural-language boundary for B1-B5; actions are synchronous and observable."""

    APP_ALIASES = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "calc": "calc.exe",
        "paint": "mspaint.exe",
        "powershell": "powershell.exe",
        "terminal": "wt.exe",
        "cmd": "cmd.exe",
        "explorer": "explorer.exe",
        "file explorer": "explorer.exe",
        "task manager": "taskmgr.exe",
        "edge": "msedge.exe",
        "chrome": "chrome.exe",
    }

    def __init__(self) -> None:
        self.system = SystemInterface()
        self.processes = ProcessDiscovery()
        self.launcher = ApplicationLauncher()
        self.windows = WindowController()
        self.keyboard = KeyboardDriver()

    @staticmethod
    def _failure(message: str, capability: str = "") -> DesktopAction:
        return DesktopAction(True, False, message, capability)

    def handle(self, text: str) -> DesktopAction:
        value = " ".join(text.strip().split())
        lowered = value.casefold()

        try:
            if lowered in {"system info", "show system info", "computer info", "pc info"}:
                snapshot = self.system.snapshot()
                return DesktopAction(True, True, str(snapshot.as_dict()), "desktop.system.read", snapshot.as_dict())

            if lowered in {"open google", "go to google", "open google.com"}:
                return DesktopAction(True, True, self.system.open_url("https://www.google.com"), "desktop.browser.open")

            url_match = re.match(r"^(?:open|go to|visit)\s+(https?://\S+)$", value, re.I)
            if url_match:
                return DesktopAction(True, True, self.system.open_url(url_match.group(1)), "desktop.browser.open")

            proc_match = re.match(r"^(?:show|list)\s+(?:running\s+)?process(?:es)?$", value, re.I)
            if proc_match:
                rows = self.processes.list(limit=20)
                msg = " | ".join(f"{p.name} ({p.pid})" for p in rows) or "No processes found."
                return DesktopAction(True, True, msg, "desktop.process.read", {"count": len(rows)})

            find_proc = re.match(r"^(?:find|search)\s+(?:the\s+)?process\s+(.+)$", value, re.I)
            if find_proc:
                rows = self.processes.find(find_proc.group(1), limit=10)
                msg = " | ".join(f"{p.name} ({p.pid})" for p in rows) or "No matching process found."
                return DesktopAction(True, True, msg, "desktop.process.read", {"count": len(rows)})

            launch = re.match(r"^(?:open|launch|start)\s+(.+)$", value, re.I)
            if launch:
                target = launch.group(1).strip().casefold()
                if target in self.APP_ALIASES:
                    result = self.launcher.launch(self.APP_ALIASES[target], authorized=True)
                    return DesktopAction(True, True, f"Started {target} (pid {result.pid}).", "desktop.app.launch", {"pid": result.pid})
                if target.startswith("http://") or target.startswith("https://"):
                    return DesktopAction(True, True, self.system.open_url(target), "desktop.browser.open")

            windows_cmd = re.match(r"^(?:show|list)\s+windows(?:\s+for\s+(.+))?$", value, re.I)
            if windows_cmd:
                rows = self.windows.list(windows_cmd.group(1) or "", limit=30)
                msg = " | ".join(f"{w.title} [{w.handle}]" for w in rows) or "No visible windows found."
                return DesktopAction(True, True, msg, "desktop.window.read", {"count": len(rows)})

            press = re.match(r"^press\s+(.+)$", value, re.I)
            if press:
                tokens = [t for t in re.split(r"\s*\+\s*|\s+", press.group(1)) if t]
                key, modifiers = tokens[-1], tuple(t for t in tokens[:-1] if t.casefold() in {"ctrl", "shift", "alt"})
                return DesktopAction(True, True, self.keyboard.press(key, modifiers), "desktop.keyboard.write")

            type_match = re.match(r"^(?:type|write)\s+(.+)$", value, re.I)
            if type_match:
                return DesktopAction(True, True, self.keyboard.type_text(type_match.group(1)), "desktop.keyboard.write")

            return DesktopAction(False, True, "")
        except Exception as exc:
            return self._failure(str(exc))
