"""Replaceable OCR provider boundary with a lightweight offline fallback."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class OCRResult:
    text: str
    confidence: float = 0.0
    provider: str = "offline"


class OCRProvider(Protocol):
    name: str
    def extract(self, image: object) -> OCRResult: ...


class OfflineOCRProvider:
    name = "offline"

    def extract(self, image: object) -> OCRResult:
        return OCRResult("", 0.0, self.name)


class OCRAdapter:
    def __init__(self, provider: OCRProvider | None = None) -> None:
        self.provider = provider or OfflineOCRProvider()

    def extract(self, image: object) -> OCRResult:
        result = self.provider.extract(image)
        if not isinstance(result, OCRResult):
            raise TypeError("OCR provider must return OCRResult")
        return result
