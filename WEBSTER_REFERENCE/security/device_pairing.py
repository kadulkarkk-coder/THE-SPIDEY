"""Secure device-pairing primitives for WEBSTER remote communication."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import secrets
from time import time


@dataclass(frozen=True)
class PairingRecord:
    device_id: str
    fingerprint: str
    created_at: float
    expires_at: float


class DevicePairing:
    """Create short-lived pairing records without storing raw secrets."""

    def __init__(self, *, ttl_seconds: int = 300) -> None:
        if ttl_seconds < 30:
            raise ValueError("ttl_seconds must be at least 30")
        self.ttl_seconds = ttl_seconds
        self._records: dict[str, PairingRecord] = {}

    def create(self, device_id: str) -> tuple[PairingRecord, str]:
        device_id = device_id.strip()
        if not device_id:
            raise ValueError("device_id must not be empty")
        code = f"{secrets.randbelow(1_000_000):06d}"
        fingerprint = sha256(f"{device_id}:{code}".encode()).hexdigest()
        now = time()
        record = PairingRecord(device_id, fingerprint, now, now + self.ttl_seconds)
        self._records[device_id] = record
        return record, code

    def verify(self, device_id: str, code: str) -> bool:
        record = self._records.get(device_id.strip())
        if record is None or time() > record.expires_at:
            return False
        fingerprint = sha256(f"{device_id.strip()}:{code}".encode()).hexdigest()
        return secrets.compare_digest(record.fingerprint, fingerprint)

    def revoke(self, device_id: str) -> None:
        self._records.pop(device_id.strip(), None)
