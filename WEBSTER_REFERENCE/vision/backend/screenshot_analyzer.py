"""Lightweight screenshot analysis contract; concrete vision models remain optional."""
from __future__ import annotations
from dataclasses import dataclass
from .ocr_adapter import OCRAdapter, OCRResult
from .visual_context import VisualContext, VisualContextBuilder


@dataclass(frozen=True)
class ScreenshotAnalysis:
    ocr: OCRResult
    context: VisualContext


class ScreenshotAnalyzer:
    def __init__(self, ocr: OCRAdapter | None = None, context_builder: VisualContextBuilder | None = None) -> None:
        self.ocr = ocr or OCRAdapter()
        self.context_builder = context_builder or VisualContextBuilder()

    def analyze(self, screenshot: object, *, description: str = "", source: str = "screenshot") -> ScreenshotAnalysis:
        result = self.ocr.extract(screenshot)
        combined = " ".join(part for part in (description, result.text) if part)
        context = self.context_builder.build(combined, source=source)
        return ScreenshotAnalysis(result, context)
