"""Lightweight entity and parameter extraction for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Entity:
    kind: str
    value: str
    source: str


@dataclass(frozen=True)
class EntityResult:
    entities: tuple[Entity, ...]


def extract_entities(text: str) -> EntityResult:
    entities: list[Entity] = []
    for value in re.findall(r"https?://[^\s]+", text):
        entities.append(Entity("url", value.rstrip(".,!?"), value))
    for value in re.findall(r"\b\d+(?:\.\d+)?\b", text):
        entities.append(Entity("number", value, value))
    return EntityResult(tuple(entities))
