"""Explicit association builder for related memory keys."""
from __future__ import annotations
from collections import defaultdict

class AssociationEngine:
    def __init__(self) -> None:
        self._links: dict[str, set[str]] = defaultdict(set)

    def link(self, left: str, right: str) -> None:
        left, right = left.strip(), right.strip()
        if not left or not right: raise ValueError("association endpoints are required")
        self._links[left].add(right)
        self._links[right].add(left)

    def related(self, key: str) -> tuple[str, ...]:
        return tuple(sorted(self._links.get(key.strip(), ())))
