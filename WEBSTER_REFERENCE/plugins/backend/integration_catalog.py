"""Catalog for optional integrations and provider-neutral capabilities."""
from __future__ import annotations

from dataclasses import dataclass
from threading import RLock


@dataclass(frozen=True)
class IntegrationSpec:
    integration_id: str
    name: str
    description: str
    capabilities: tuple[str, ...] = ()
    requires_network: bool = False
    optional: bool = True


class IntegrationCatalog:
    """Thread-safe catalog; registration never makes an integration mandatory."""

    def __init__(self) -> None:
        self._items: dict[str, IntegrationSpec] = {}
        self._lock = RLock()

    def register(self, spec: IntegrationSpec) -> IntegrationSpec:
        with self._lock:
            if spec.integration_id in self._items:
                raise ValueError(f"integration already registered: {spec.integration_id}")
            self._items[spec.integration_id] = spec
        return spec

    def get(self, integration_id: str) -> IntegrationSpec:
        with self._lock:
            return self._items[integration_id]

    def find_capability(self, capability: str) -> tuple[IntegrationSpec, ...]:
        capability = capability.strip()
        with self._lock:
            return tuple(item for item in self._items.values() if capability in item.capabilities)

    def list(self) -> tuple[IntegrationSpec, ...]:
        with self._lock:
            return tuple(self._items.values())
