"""Validated image ingestion metadata boundary for WEBSTER."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ImageInput:
    source: str
    media_type: str = "image/unknown"
    width: int | None = None
    height: int | None = None
    size_bytes: int = 0


class ImageInputValidator:
    ALLOWED_TYPES = frozenset({"image/png", "image/jpeg", "image/webp", "image/gif", "image/bmp"})

    def validate(self, image: ImageInput) -> ImageInput:
        source = image.source.strip()
        media_type = image.media_type.strip().lower()
        if not source:
            raise ValueError("image source is required")
        if media_type not in self.ALLOWED_TYPES:
            raise ValueError(f"unsupported image type: {media_type}")
        if image.width is not None and image.width < 1:
            raise ValueError("image width must be positive")
        if image.height is not None and image.height < 1:
            raise ValueError("image height must be positive")
        if image.size_bytes < 0:
            raise ValueError("image size cannot be negative")
        return ImageInput(source, media_type, image.width, image.height, image.size_bytes)

    def from_path(self, path: str, media_type: str) -> ImageInput:
        value = Path(path).expanduser()
        if not value.is_file():
            raise FileNotFoundError(str(value))
        item = ImageInput(str(value), media_type, size_bytes=value.stat().st_size)
        return self.validate(item)
