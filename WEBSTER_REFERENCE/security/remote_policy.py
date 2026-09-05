"""Policy boundary for remote phone-to-WEBSTER requests."""
from __future__ import annotations

from enum import Enum


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RemotePolicy:
    """Allow safe conversational requests while requiring approval for risky actions."""

    def __init__(self) -> None:
        self._approved_devices: set[str] = set()

    def approve_device(self, device_id: str) -> None:
        device_id = device_id.strip()
        if not device_id:
            raise ValueError("device_id must not be empty")
        self._approved_devices.add(device_id)

    def revoke_device(self, device_id: str) -> None:
        self._approved_devices.discard(device_id.strip())

    def device_allowed(self, device_id: str) -> bool:
        return device_id.strip() in self._approved_devices

    def requires_confirmation(self, risk: RiskLevel) -> bool:
        return risk in {RiskLevel.MEDIUM, RiskLevel.HIGH}
