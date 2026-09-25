"""Static safety checks for proposed evolved plugins."""
from __future__ import annotations

from dataclasses import dataclass

from .plugin_manifest import EvolutionPluginManifest


@dataclass(frozen=True)
class ValidationReport:
    valid: bool
    errors: tuple[str, ...] = ()


class EvolutionValidator:
    """Reject incomplete or unsafe manifests before installation."""

    def validate(self, manifest: EvolutionPluginManifest) -> ValidationReport:
        errors: list[str] = []
        if not manifest.tests:
            errors.append("evolved plugin must declare at least one test")
        if not manifest.rollback_version:
            errors.append("rollback_version is required")
        if any(permission.startswith("system:write") for permission in manifest.permissions):
            errors.append("system write permission requires explicit approval")
        for key in ("cpu", "memory"):
            value = manifest.resource_limits.get(key, "").strip()
            if not value:
                errors.append(f"resource limit missing: {key}")
        return ValidationReport(not errors, tuple(errors))
