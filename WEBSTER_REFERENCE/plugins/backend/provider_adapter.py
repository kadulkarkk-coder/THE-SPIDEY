"""Provider adapter contracts for optional WEBSTER integrations."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ProviderRequest:
    """Small, provider-neutral request envelope."""

    operation: str
    payload: str


@dataclass(frozen=True)
class ProviderResponse:
    """Normalized provider result."""

    success: bool
    content: str = ""
    provider: str = "local"
    error: str = ""


class ProviderAdapter(Protocol):
    """Optional integration boundary; WEBSTER does not depend on a provider."""

    provider_id: str

    def handle(self, request: ProviderRequest) -> ProviderResponse:
        ...
