"""Retention and sensitivity policy for WEBSTER memory."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class MemoryPolicy:
    retain: bool = True
    sensitive: bool = False
    ttl_seconds: int | None = None

class MemoryPolicyEngine:
    def decide(self, *, kind: str, sensitive: bool = False, ttl_seconds: int | None = None) -> MemoryPolicy:
        kind = kind.strip().lower()
        retain = kind not in {"temporary", "ephemeral"}
        return MemoryPolicy(retain=retain, sensitive=sensitive, ttl_seconds=ttl_seconds)
