"""Registry for provenance/source metadata used by memory and knowledge."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Source:
    name: str
    kind: str = "unknown"
    trust: float = 0.5

class SourceRegistry:
    def __init__(self) -> None:
        self._sources: dict[str, Source] = {}

    def register(self, name: str, *, kind: str = "unknown", trust: float = 0.5) -> Source:
        source = Source(name.strip(), kind.strip(), max(0.0, min(1.0, trust)))
        if not source.name: raise ValueError("source name is required")
        self._sources[source.name] = source
        return source

    def get(self, name: str) -> Source | None:
        return self._sources.get(name.strip())
