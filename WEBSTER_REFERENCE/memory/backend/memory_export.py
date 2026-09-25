"""Portable, JSON-safe memory export."""
from __future__ import annotations
from dataclasses import asdict
from datetime import datetime
import json
from .memory_store import MemoryStore

class MemoryExporter:
    def export(self, store: MemoryStore) -> str:
        records = []
        for record in store.all():
            data = asdict(record)
            data["created_at"] = record.created_at.isoformat()
            records.append(data)
        return json.dumps(records, ensure_ascii=False, default=str, sort_keys=True)
