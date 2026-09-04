"""Application-layer gateway between a phone client and WEBSTER core."""
from __future__ import annotations

from collections.abc import Callable

from .device_registry import DeviceRegistry
from .remote_policy import RemotePolicy
from .remote_session import RemoteSession
from .remote_types import RemoteRequest, RemoteResponse, RemoteStatus


class RemoteGateway:
    """Validate remote envelopes, then hand text to the existing WEBSTER runtime."""

    def __init__(self, *, devices: DeviceRegistry | None = None,
                 session: RemoteSession | None = None,
                 policy: RemotePolicy | None = None) -> None:
        self.devices = devices or DeviceRegistry()
        self.session = session or RemoteSession()
        self.policy = policy or RemotePolicy()

    def handle(self, request: RemoteRequest, executor: Callable[[str], str]) -> RemoteResponse:
        if not self.devices.trusted(request.device_id):
            return RemoteResponse(request.request_id, False, "Device is not paired.", RemoteStatus.OFFLINE)
        if not self.policy.allowed(request.channel.value):
            return RemoteResponse(request.request_id, False, "Remote channel is disabled.", RemoteStatus.ONLINE)
        self.session.touch()
        try:
            result = executor(request.text)
        except Exception as exc:
            return RemoteResponse(request.request_id, False, f"WEBSTER could not complete the request: {exc}", RemoteStatus.ONLINE)
        return RemoteResponse(request.request_id, True, result, RemoteStatus.ONLINE)
