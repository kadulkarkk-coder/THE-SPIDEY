"""Lightweight observable local system information."""
from __future__ import annotations
from dataclasses import dataclass
import os, platform, shutil

@dataclass(frozen=True)
class SystemInfo:
    platform: str
    release: str
    machine: str
    python: str
    cpu_count: int
    memory_bytes: int | None
    disk_free_bytes: int | None

class SystemInfoProvider:
    def collect(self) -> SystemInfo:
        memory = None
        try:
            if hasattr(os, "sysconf"):
                pages = os.sysconf("SC_PHYS_PAGES"); size = os.sysconf("SC_PAGE_SIZE")
                memory = pages * size
        except (ValueError, OSError): pass
        try: free = shutil.disk_usage(os.getcwd()).free
        except OSError: free = None
        return SystemInfo(platform.system(), platform.release(), platform.machine(), platform.python_version(), os.cpu_count() or 1, memory, free)
