"""B1 real local Windows/system interface for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import os
import platform
import shutil
import webbrowser


@dataclass(frozen=True)
class SystemSnapshot:
    platform: str
    release: str
    machine: str
    python: str
    cpu_count: int
    cwd: str
    disk_free_gb: float

    def as_dict(self) -> dict[str, object]:
        return {
            "platform": self.platform,
            "release": self.release,
            "machine": self.machine,
            "python": self.python,
            "cpu_count": self.cpu_count,
            "cwd": self.cwd,
            "disk_free_gb": self.disk_free_gb,
        }


class SystemInterface:
    """Small, synchronous system boundary with no background polling."""

    def snapshot(self) -> SystemSnapshot:
        usage = shutil.disk_usage(os.getcwd())
        return SystemSnapshot(
            platform.system(),
            platform.release(),
            platform.machine(),
            platform.python_version(),
            os.cpu_count() or 1,
            os.getcwd(),
            round(usage.free / (1024 ** 3), 2),
        )

    def open_url(self, url: str) -> str:
        value = url.strip()
        if not (value.startswith("https://") or value.startswith("http://")):
            raise ValueError("Only http:// and https:// URLs are allowed.")
        if any(ch in value for ch in ("\r", "\n", "\x00")):
            raise ValueError("Invalid URL.")
        if not webbrowser.open(value):
            raise RuntimeError("The operating system did not accept the URL.")
        return f"Opened {value}"

    def local_time(self) -> str:
        now = datetime.now().astimezone()
        return now.strftime("%H:%M:%S | %Y-%m-%d")
