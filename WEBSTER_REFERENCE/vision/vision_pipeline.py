"""Controlled multimodal visual processing pipeline for WEBSTER."""
from __future__ import annotations
from dataclasses import dataclass
from .image_input import ImageInput, ImageInputValidator
from .ocr_adapter import OCRAdapter, OCRResult
from .visual_context import VisualContext, VisualContextBuilder
from .multimodal_router import ModalityRequest, MultimodalRouter
from .vision_permissions import VisionPermissions


@dataclass(frozen=True)
class VisionResult:
    modality: str
    ocr: OCRResult
    context: VisualContext


class VisionPipeline:
    def __init__(self, *, permissions: VisionPermissions | None = None, ocr: OCRAdapter | None = None) -> None:
        self.permissions = permissions or VisionPermissions()
        self.input_validator = ImageInputValidator()
        self.ocr = ocr or OCRAdapter()
        self.context_builder = VisualContextBuilder()
        self.router = MultimodalRouter()
        for modality in ("image", "screenshot", "document"):
            self.router.register(modality, "vision")

    def process(self, principal: str, image: ImageInput, *, modality: str = "image", description: str = "") -> VisionResult:
        capability = f"analyze_{modality.strip().lower()}"
        if not self.permissions.allowed(principal, capability):
            raise PermissionError(f"vision capability is not permitted: {capability}")
        validated = self.input_validator.validate(image)
        route = self.router.route(ModalityRequest(modality, validated))
        if route is None:
            raise ValueError(f"unsupported modality: {modality}")
        result = self.ocr.extract(validated)
        combined = " ".join(part for part in (description, result.text) if part)
        context = self.context_builder.build(combined, source=modality)
        return VisionResult(route.modality, result, context)
