"""B2 read-only process discovery."""
from __future__ import annotations

from dataclasses import dataclass
import os
import subprocess


@dataclass(frozen=True)
class ProcessMatch:
    pid: int
    name: str

    def as_dict(self) -> dict[str, object]:
        return {"pid": self.pid, "name": self.name}


class ProcessDiscovery:
    """Enumerates processes without terminating or mutating them."""

    def list(self, query: str = "", limit: int = 20) -> tuple[ProcessMatch, ...]:
        limit = max(1, min(int(limit), 100))
        if os.name == "nt":
            result = subprocess.run(
                ["tasklist", "/FO", "CSV", "/NH"],
                capture_output=True, text=True, timeout=5, check=False,
            )
            rows: list[ProcessMatch] = []
            for line in result.stdout.splitlines():
                parts = [p.strip('"') for p in line.split('","')]
                if len(parts) < 2:
                    continue
                try:
                    pid = int(parts[1])
                except ValueError:
                    continue
                name = parts[0]
                if not query or query.casefold() in name.casefold():
                    rows.append(ProcessMatch(pid, name))
            return tuple(rows[:limit])

        result = subprocess.run(
            ["ps", "-eo", "pid=,comm="],
            capture_output=True, text=True, timeout=5, check=False,
        )
        rows = []
        for line in result.stdout.splitlines():
            parts = line.strip().split(None, 1)
            if len(parts) != 2:
                continue
            try:
                pid = int(parts[0])
            except ValueError:
                continue
            if not query or query.casefold() in parts[1].casefold():
                rows.append(ProcessMatch(pid, parts[1]))
        return tuple(rows[:limit])

    def find(self, query: str, limit: int = 10) -> tuple[ProcessMatch, ...]:
        value = query.strip()
        if len(value) < 2:
            raise ValueError("Process search requires at least 2 characters.")
        return self.list(value, limit)
