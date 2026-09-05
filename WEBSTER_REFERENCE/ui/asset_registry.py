"""External UI asset registry for WEBSTER."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class UIAsset:
    name: str
    path: str
    kind: str


class AssetRegistry:
    """Resolve generated assets without loading image bytes into memory."""

    def __init__(self, root: str | Path = "assets") -> None:
        self.root = Path(root)
        self._assets: dict[str, UIAsset] = {}

    def register(self, name: str, relative_path: str, kind: str = "image") -> UIAsset:
        if not name.strip() or not relative_path.strip():
            raise ValueError("asset name and path must not be empty")
        asset = UIAsset(name.strip(), relative_path.replace("\\", "/"), kind.strip() or "image")
        self._assets[asset.name] = asset
        return asset

    def get(self, name: str) -> UIAsset:
        return self._assets[name]

    def resolve(self, name: str) -> Path:
        asset = self.get(name)
        return self.root / asset.path

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._assets))
