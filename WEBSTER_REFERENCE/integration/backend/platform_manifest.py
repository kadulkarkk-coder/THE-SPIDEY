"""Cross-platform integration metadata for WEBSTER clients."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlatformManifest:
    """Describes a supported WEBSTER client without binding the core to a UI toolkit."""

    name: str = "WEBSTER"
    windows_client: str = "WEBSTER.exe"
    android_client: str = "WEBSTER.apk"
    identity_provider: str = "google-oauth"
    offline_first: bool = True
    gesture_on_windows: bool = True
    gesture_on_android: bool = False

    def supports(self, platform: str) -> bool:
        return platform.strip().lower() in {"windows", "android"}
