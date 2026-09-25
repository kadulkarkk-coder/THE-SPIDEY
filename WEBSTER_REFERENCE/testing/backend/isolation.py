"""Deterministic isolation helpers for WEBSTER test execution."""
from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from typing import Iterator


@contextmanager
def isolated_mapping(mapping: dict) -> Iterator[dict]:
    """Yield an independent copy so a test cannot mutate its caller's mapping."""
    snapshot = deepcopy(mapping)
    yield snapshot


class IsolationError(RuntimeError):
    """Raised when an isolated test contract is violated."""


def assert_unchanged(before: dict, after: dict) -> None:
    """Assert that a protected mapping has not been mutated by a test."""
    if before != after:
        raise IsolationError("protected test state was mutated")
