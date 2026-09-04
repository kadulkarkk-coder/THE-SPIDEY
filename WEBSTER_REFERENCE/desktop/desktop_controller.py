"""High-level, permission-aware coordinator for desktop capabilities."""
from __future__ import annotations
from .desktop_permissions import DesktopPermissions
from .desktop_observer import DesktopObserver

class DesktopController:
    def __init__(self, permissions: DesktopPermissions | None = None, observer: DesktopObserver | None = None) -> None:
        self.permissions = permissions or DesktopPermissions()
        self.observer = observer or DesktopObserver()

    def authorize(self, principal: str, capability: str) -> None:
        self.permissions.grant(principal, capability)

    def check(self, principal: str, capability: str) -> bool:
        return self.permissions.allowed(principal, capability)

    def plan(self, principal: str, capability: str, target: str = "") -> dict[str, str]:
        if not self.check(principal, capability):
            self.observer.record(capability, principal, False, "permission denied")
            raise PermissionError(f"desktop capability not permitted: {capability}")
        item = {"principal": principal.strip(), "capability": capability.strip().lower(), "target": target.strip()}
        self.observer.record(capability, principal, True, "operation planned")
        return item
