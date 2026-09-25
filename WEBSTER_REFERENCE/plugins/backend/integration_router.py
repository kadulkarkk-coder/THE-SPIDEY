"""Provider-neutral routing for optional WEBSTER integrations."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .integration_catalog import IntegrationCatalog


@dataclass(frozen=True)
class RouteDecision:
    integration_id: str
    available: bool
    reason: str


class IntegrationRouter:
    """Choose an available integration without making external services required."""

    def __init__(self, catalog: IntegrationCatalog) -> None:
        self.catalog = catalog
        self._handlers: dict[str, Callable[[str], str]] = {}

    def bind(self, integration_id: str, handler: Callable[[str], str]) -> None:
        self.catalog.get(integration_id)
        self._handlers[integration_id] = handler

    def choose(self, capability: str, *, network_available: bool = True) -> RouteDecision | None:
        for spec in self.catalog.find_capability(capability):
            if spec.requires_network and not network_available:
                continue
            if spec.integration_id in self._handlers:
                return RouteDecision(spec.integration_id, True, "handler available")
        return None

    def invoke(self, decision: RouteDecision, payload: str) -> str:
        if not decision.available or decision.integration_id not in self._handlers:
            raise RuntimeError(f"integration unavailable: {decision.integration_id}")
        return self._handlers[decision.integration_id](payload)
