"""Stable JSON serialization for memory records."""
from __future__ import annotations
import json
from dataclasses import asdict
from .memory_store import MemoryRecord

class MemorySerializer:
    def dumps(self, record: MemoryRecord) -> str:
        data = asdict(record)
        data["created_at"] = record.created_at.isoformat()
        return json.dumps(data, ensure_ascii=False, sort_keys=True, default=str)
