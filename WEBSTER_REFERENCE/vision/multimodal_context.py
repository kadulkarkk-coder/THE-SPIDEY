"""Normalized context object for combining visual and textual inputs."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class MultimodalContext:
    text: str = ""
    visual: str = ""
    sources: tuple[str, ...] = ()

    @property
    def combined(self) -> str:
        parts = tuple(part.strip() for part in (self.text, self.visual) if part.strip())
        return " ".join(parts)


class MultimodalContextBuilder:
    def build(self, *, text: str = "", visual: str = "", sources: tuple[str, ...] = ()) -> MultimodalContext:
        normalized_sources = tuple(sorted({source.strip().lower() for source in sources if source.strip()}))
        return MultimodalContext(" ".join(text.split()), " ".join(visual.split()), normalized_sources)
