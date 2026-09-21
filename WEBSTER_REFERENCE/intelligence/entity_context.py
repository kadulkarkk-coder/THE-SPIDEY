"""Persistent conversational entity context for WEBSTER A13."""
from __future__ import annotations
from dataclasses import dataclass
from time import monotonic
import re

@dataclass(frozen=True)
class ContextEntity:
    name: str
    value: str
    source_task_id: str = ""
    turn: int = 0
    created_at: float = 0.0

class EntityContext:
    """Small session-local reference frame with explicit expiry and replacement rules."""

    def __init__(self, ttl_seconds: float = 900.0, max_entities: int = 16) -> None:
        self.ttl_seconds = max(30.0, ttl_seconds)
        self.max_entities = max(1, max_entities)
        self._entities: dict[str, ContextEntity] = {}
        self._turn = 0

    def observe(self, text: str, *, task_id: str = "") -> None:
        self._turn += 1
        now = monotonic()
        self.expire()
        number_matches = re.findall(r"(?<![\d.])-?\d+(?:\.\d+)?(?![\d.])", text)
        if number_matches:
            value = number_matches[-1]
            self._entities["last_number"] = ContextEntity("last_number", value, task_id, self._turn, now)
        if task_id:
            self._entities["last_task"] = ContextEntity("last_task", task_id, task_id, self._turn, now)
        self._trim()

    def set(self, name: str, value: str, *, task_id: str = "") -> None:
        self._turn += 1
        self._entities[name] = ContextEntity(name, str(value), task_id, self._turn, monotonic())
        self._trim()

    def resolve(self, reference: str) -> ContextEntity | None:
        self.expire()
        key = self._normalize(reference)
        if key in {"it", "that", "this", "the result", "that result", "the number", "that number"}:
            return self._entities.get("last_number") or self._entities.get("last_task")
        return self._entities.get(key)

    def invalidate(self, *names: str) -> None:
        for name in names:
            self._entities.pop(self._normalize(name), None)

    def expire(self) -> None:
        cutoff = monotonic() - self.ttl_seconds
        self._entities = {k: v for k, v in self._entities.items() if v.created_at >= cutoff}

    def snapshot(self) -> dict[str, str]:
        self.expire()
        return {key: value.value for key, value in self._entities.items()}

    @staticmethod
    def _normalize(value: str) -> str:
        return " ".join(value.lower().strip().split())

    def _trim(self) -> None:
        if len(self._entities) <= self.max_entities:
            return
        ordered = sorted(self._entities.items(), key=lambda item: item[1].created_at, reverse=True)
        self._entities = dict(ordered[: self.max_entities])
