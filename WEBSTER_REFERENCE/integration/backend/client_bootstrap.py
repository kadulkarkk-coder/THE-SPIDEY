"""Product bootstrap contract for the Windows and Android WEBSTER clients."""
from __future__ import annotations

from dataclasses import dataclass

from .platform_manifest import PlatformManifest
from .resource_policy import ResourcePolicy


@dataclass(frozen=True)
class ClientBootstrap:
    platform: str
    manifest: PlatformManifest
    resources: ResourcePolicy

    @classmethod
    def for_platform(cls, platform: str) -> "ClientBootstrap":
        normalized = platform.strip().lower()
        manifest = PlatformManifest()
        if not manifest.supports(normalized):
            raise ValueError(f"unsupported platform: {platform}")
        resources = ResourcePolicy()
        resources.validate()
        return cls(normalized, manifest, resources)

    @property
    def offline_ready(self) -> bool:
        return self.manifest.offline_first
