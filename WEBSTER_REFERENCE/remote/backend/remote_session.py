"""Low-bandwidth remote session state for phone-to-laptop control."""
from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from time import monotonic

from .remote_types import RemoteStatus


@dataclass(frozen=True)
class RemoteSessionSnapshot:
    device_id: str | None
    status: RemoteStatus
    last_activity: float | None


class RemoteSession:
    """Tracks connection state only; it does not open network sockets."""

    def __init__(self) -> None:
        self._device_id: str | None = None
        self._status = RemoteStatus.OFFLINE
        self._last_activity: float | None = None
        self._lock = RLock()

    def connect(self, device_id: str) -> None:
        if not device_id.strip():
            raise ValueError("device_id must not be empty")
        with self._lock:
            self._device_id = device_id
            self._status = RemoteStatus.ONLINE
            self._last_activity = monotonic()

    def disconnect(self) -> None:
        with self._lock:
            self._status = RemoteStatus.OFFLINE

    def touch(self) -> None:
        with self._lock:
            self._last_activity = monotonic()

    def snapshot(self) -> RemoteSessionSnapshot:
        with self._lock:
            return RemoteSessionSnapshot(self._device_id, self._status, self._last_activity)
