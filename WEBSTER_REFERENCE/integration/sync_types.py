"""Provider-neutral sync contracts for WEBSTER devices."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from time import time
from typing import Mapping


class SyncStatus(str, Enum):
    LOCAL = "local"
    QUEUED = "queued"
    SYNCED = "synced"
    CONFLICT = "conflict"


@dataclass(frozen=True)
class SyncRecord:
    record_id: str
    kind: str
    payload: Mapping[str, str] = field(default_factory=dict)
    device_id: str = ""
    timestamp: float = field(default_factory=time)
    status: SyncStatus = SyncStatus.LOCAL
