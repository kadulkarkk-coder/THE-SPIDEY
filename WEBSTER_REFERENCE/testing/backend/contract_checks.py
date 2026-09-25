"""Reusable, dependency-free contract checks for WEBSTER subsystems."""
from __future__ import annotations

from collections.abc import Callable


def require(condition: bool, message: str) -> None:
    """Raise AssertionError with a useful contract failure message."""
    if not condition:
        raise AssertionError(message)


def require_callable(value: object, name: str) -> None:
    require(callable(value), f"{name} must be callable")


def require_non_empty_text(value: object, name: str) -> None:
    require(isinstance(value, str) and bool(value.strip()), f"{name} must be non-empty text")


def check_factory(factory: Callable[[], object], name: str) -> None:
    """Verify that a lightweight subsystem factory can be constructed."""
    require_callable(factory, name)
    instance = factory()
    require(instance is not None, f"{name} returned None")
