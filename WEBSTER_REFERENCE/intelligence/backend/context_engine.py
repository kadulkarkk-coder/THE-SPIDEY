"""Privacy-aware context assembly for WEBSTER requests."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ContextItem:
    key: str
    value: Any
    sensitive: bool = False


class ContextEngine:
    """Builds bounded context while allowing sensitive values to be excluded."""

    def assemble(self, items: list[ContextItem], *, include_sensitive: bool = False) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for item in items:
            if item.sensitive and not include_sensitive:
                continue
            result[item.key] = item.value
        return result
