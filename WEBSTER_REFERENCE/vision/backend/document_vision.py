"""Lightweight document-vision analysis boundary for WEBSTER."""
from __future__ import annotations
from dataclasses import dataclass
from .ocr_adapter import OCRAdapter, OCRResult
from .visual_context import VisualContext, VisualContextBuilder


@dataclass(frozen=True)
class DocumentAnalysis:
    ocr: OCRResult
    context: VisualContext
    pages: int = 1


class DocumentVision:
    """Combine document metadata, OCR and visual context without requiring a model."""

    def __init__(self, ocr: OCRAdapter | None = None, context_builder: VisualContextBuilder | None = None) -> None:
        self.ocr = ocr or OCRAdapter()
        self.context_builder = context_builder or VisualContextBuilder()

    def analyze(self, document: object, *, description: str = "", pages: int = 1) -> DocumentAnalysis:
        if pages < 1:
            raise ValueError("pages must be positive")
        result = self.ocr.extract(document)
        combined = " ".join(part for part in (description, result.text) if part)
        context = self.context_builder.build(combined, source="document")
        return DocumentAnalysis(result, context, pages)
