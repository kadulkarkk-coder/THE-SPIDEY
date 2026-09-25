"""Small integration checks for WEBSTER's major contracts."""
from __future__ import annotations

from .contract_checks import require, require_callable


def check_event_bus(bus: object) -> None:
    """Verify an event bus exposes subscribe/publish behavior."""
    require_callable(getattr(bus, "subscribe", None), "event_bus.subscribe")
    require_callable(getattr(bus, "publish", None), "event_bus.publish")


def check_registry(registry: object) -> None:
    """Verify registries expose registration and lookup operations."""
    require_callable(getattr(registry, "register", None), "registry.register")
    lookup = getattr(registry, "get", None)
    if lookup is None:
        lookup = getattr(registry, "find", None)
    require_callable(lookup, "registry.lookup")


def check_pipeline(pipeline: object) -> None:
    """Verify a subsystem pipeline has an explicit execution entry point."""
    run = getattr(pipeline, "run", None)
    if run is None:
        run = getattr(pipeline, "process", None)
    require_callable(run, "pipeline.run/process")
