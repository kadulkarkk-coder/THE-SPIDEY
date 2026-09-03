"""Read-only process observation with explicit termination authorization."""
from __future__ import annotations
from dataclasses import dataclass
import os, subprocess

@dataclass(frozen=True)
class ProcessInfo:
    pid: int
    name: str

class ProcessManager:
    def list(self) -> tuple[ProcessInfo, ...]:
        if os.name == "nt":
            result = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True, timeout=5)
            rows = []
            for line in result.stdout.splitlines():
                parts = [p.strip('"') for p in line.split('","')]
                if len(parts) >= 2:
                    try: rows.append(ProcessInfo(int(parts[1]), parts[0]))
                    except ValueError: pass
            return tuple(rows)
        result = subprocess.run(["ps", "-eo", "pid=,comm="], capture_output=True, text=True, timeout=5)
        rows = []
        for line in result.stdout.splitlines():
            parts = line.strip().split(None, 1)
            if len(parts) == 2:
                try: rows.append(ProcessInfo(int(parts[0]), parts[1]))
                except ValueError: pass
        return tuple(rows)

    def terminate(self, pid: int, *, authorized: bool = False) -> None:
        if pid <= 0: raise ValueError("pid must be positive")
        if not authorized: raise PermissionError("process termination requires explicit authorization")
        os.kill(pid, 15)
