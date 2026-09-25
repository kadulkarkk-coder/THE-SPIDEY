"""Explicit executable launch boundary; no shell parsing is used."""
from __future__ import annotations
from dataclasses import dataclass
import subprocess

@dataclass(frozen=True)
class LaunchResult:
    executable: str
    pid: int | None

class ApplicationLauncher:
    def launch(self, executable: str, args: tuple[str, ...] = (), *, authorized: bool = False) -> LaunchResult:
        program = executable.strip()
        if not program: raise ValueError("executable is required")
        if not authorized: raise PermissionError("application launch requires explicit authorization")
        if any("\x00" in arg for arg in args): raise ValueError("invalid launch argument")
        process = subprocess.Popen([program, *args], shell=False)
        return LaunchResult(program, process.pid)
