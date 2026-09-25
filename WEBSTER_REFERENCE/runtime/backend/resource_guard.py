"""Lightweight resource guard for the desktop runtime."""
from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceSnapshot:
    thread_count: int
    cpu_percent: float | None
    memory_mb: float | None


class ResourceGuard:
    """Observe resources on demand; it never starts a polling thread."""

    def snapshot(self) -> ResourceSnapshot:
        cpu = memory = None
        try:
            import psutil  # type: ignore
            process = psutil.Process(os.getpid())
            cpu = float(process.cpu_percent(interval=None))
            memory = process.memory_info().rss / (1024 * 1024)
        except Exception:
            pass
        return ResourceSnapshot(threading.active_count(), cpu, memory)

    def budget_ok(self, *, max_threads: int = 32, max_memory_mb: float | None = 1024) -> bool:
        snap = self.snapshot()
        if snap.thread_count > max_threads:
            return False
        return snap.memory_mb is None or max_memory_mb is None or snap.memory_mb <= max_memory_mb
