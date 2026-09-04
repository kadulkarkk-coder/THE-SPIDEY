"""Controlled multimodal visual processing pipeline for WEBSTER."""
from __future__ import annotations
from dataclasses import dataclass
from .image_input import ImageInput, ImageInputValidator
from .ocr_adapter import OCRAdapter, OCRResult
from .visual_context import VisualContext, VisualContextBuilder
from .multimodal_router import ModalityRequest, MultimodalRouter
from .vision_permissions import VisionPermissions
from .vision_observer import VisionObserver
from .vision_metrics import VisionMetrics


@dataclass(frozen=True)
class VisionResult:
    modality: str
    ocr: OCRResult
    context: VisualContext


class VisionPipeline:
    def __init__(self, *, permissions: VisionPermissions | None = None, ocr: OCRAdapter | None = None,
                 observer: VisionObserver | None = None, metrics: VisionMetrics | None = None) -> None:
        self.permissions = permissions or VisionPermissions()
        self.input_validator = ImageInputValidator()
        self.ocr = ocr or OCRAdapter()
        self.context_builder = VisualContextBuilder()
        self.router = MultimodalRouter()
        self.observer = observer or VisionObserver()
        self.metrics = metrics or VisionMetrics()
        for modality in ("image", "screenshot", "document"):
            self.router.register(modality, "vision")

    def process(self, principal: str, image: ImageInput, *, modality: str = "image", description: str = "") -> VisionResult:
        modality = modality.strip().lower()
        try:
            capability = f"analyze_{modality}"
            if not self.permissions.allowed(principal, capability):
                raise PermissionError(f"vision capability is not permitted: {capability}")
            validated = self.input_validator.validate(image)
            route = self.router.route(ModalityRequest(modality, validated))
            if route is None:
                raise ValueError(f"unsupported modality: {modality}")
            result = self.ocr.extract(validated)
            combined = " ".join(part for part in (description, result.text) if part)
            context = self.context_builder.build(combined, source=modality)
            output = VisionResult(route.modality, result, context)
            self.observer.record("process", modality, True, f"provider={result.provider}")
            self.metrics.record(True)
            return output
        except Exception as exc:
            self.observer.record("process", modality, False, str(exc))
            self.metrics.record(False)
            raise
