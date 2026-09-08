"""Cheap, deterministic startup checks; no network or background polling."""
from __future__ import annotations

import importlib.util
import os
import platform
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class StartupCheck:
    name: str
    ok: bool
    detail: str


class StartupChecks:
    """Validate only prerequisites WEBSTER can safely inspect locally."""

    def run(self) -> list[StartupCheck]:
        return [
            StartupCheck("python", sys.version_info >= (3, 10), platform.python_version()),
            StartupCheck("platform", os.name in {"nt", "posix"}, os.name),
            StartupCheck("writable_temp", self._writable_temp(), "temporary directory access"),
            StartupCheck("tkinter", importlib.util.find_spec("tkinter") is not None, "optional native GUI dependency"),
        ]

    @staticmethod
    def _writable_temp() -> bool:
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(prefix="webster-check-", delete=True):
                return True
        except OSError:
            return False

    def summary(self) -> dict[str, object]:
        checks = self.run()
        return {
            "ok": all(item.ok for item in checks),
            "checks": [item.__dict__ for item in checks],
        }
