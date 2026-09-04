"""Route supported modalities into shared, inspectable vision interfaces."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class ModalityRequest:
    modality: str
    payload: object


@dataclass(frozen=True)
class ModalityRoute:
    modality: str
    handler: str


class MultimodalRouter:
    def __init__(self) -> None:
        self._handlers: dict[str, str] = {}

    def register(self, modality: str, handler: str) -> None:
        key, value = modality.strip().lower(), handler.strip()
        if not key or not value:
            raise ValueError("modality and handler are required")
        self._handlers[key] = value

    def route(self, request: ModalityRequest) -> ModalityRoute | None:
        key = request.modality.strip().lower()
        handler = self._handlers.get(key)
        return ModalityRoute(key, handler) if handler else None

    def modalities(self) -> tuple[str, ...]:
        return tuple(sorted(self._handlers))
