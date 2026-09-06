"""Final release validation checks for WEBSTER Mark D."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReleaseCheck:
    name: str
    passed: bool
    message: str


class ReleaseValidator:
    """Small, dependency-free validator for the reference release layout."""

    REQUIRED = (
        "core",
        "intelligence",
        "memory",
        "agents",
        "tools",
        "automation",
        "browser",
        "desktop",
        "voice",
        "vision",
        "gesture",
        "orb",
        "widgets",
        "ui",
        "security",
        "plugins",
        "evolution",
        "testing",
        "integration",
    )

    def validate(self, root: str | Path) -> tuple[ReleaseCheck, ...]:
        base = Path(root)
        checks: list[ReleaseCheck] = []
        for name in self.REQUIRED:
            path = base / name
            checks.append(ReleaseCheck(name, path.is_dir(), "present" if path.is_dir() else "missing"))
        manifest = base / "integration" / "release_manifest.json"
        checks.append(ReleaseCheck("release_manifest", manifest.is_file(), "present" if manifest.is_file() else "missing"))
        return tuple(checks)

    def passed(self, root: str | Path) -> bool:
        return all(check.passed for check in self.validate(root))
