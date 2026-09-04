"""Pairing registry for trusted WEBSTER Anywhere devices."""
from __future__ import annotations

from dataclasses import dataclass
from threading import RLock


@dataclass(frozen=True)
class RemoteDevice:
    device_id: str
    name: str
    enabled: bool = True


class DeviceRegistry:
    """In-memory registry; persistence can be supplied by a later security phase."""

    def __init__(self) -> None:
        self._devices: dict[str, RemoteDevice] = {}
        self._lock = RLock()

    def pair(self, device_id: str, name: str) -> RemoteDevice:
        if not device_id.strip() or not name.strip():
            raise ValueError("device_id and name must not be empty")
        device = RemoteDevice(device_id.strip(), name.strip())
        with self._lock:
            self._devices[device.device_id] = device
        return device

    def revoke(self, device_id: str) -> None:
        with self._lock:
            self._devices.pop(device_id, None)

    def trusted(self, device_id: str) -> bool:
        with self._lock:
            device = self._devices.get(device_id)
            return device is not None and device.enabled

    def snapshot(self) -> tuple[RemoteDevice, ...]:
        with self._lock:
            return tuple(self._devices.values())
