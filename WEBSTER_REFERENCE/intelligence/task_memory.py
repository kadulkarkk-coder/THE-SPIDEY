"""Bounded local task memory for WEBSTER A8."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from threading import RLock
from typing import Any

@dataclass(frozen=True)
class TaskMemory:
    task_id: str
    goal: str
    status: str
    results: tuple[str, ...]
    error: str
    timestamp: str

class TaskMemoryStore:
    """Small JSON-backed task memory with atomic replacement and bounded history."""

    def __init__(self, path: str | Path | None = None, max_records: int = 100) -> None:
        if max_records < 1:
            raise ValueError("max_records must be positive")
        self.path = Path(path) if path else Path.home() / ".webster" / "task_memory.json"
        self.max_records = max_records
        self._lock = RLock()
        self._records: list[TaskMemory] = []
        self._load()

    def remember(self, task_id: str, goal: str, status: str, results: list[str] | tuple[str, ...] = (), error: str = "") -> TaskMemory:
        record = TaskMemory(
            task_id.strip(), " ".join(goal.split())[:2000], status.strip().lower(),
            tuple(str(x)[:1000] for x in results)[-20:], str(error)[:1000],
            datetime.now(timezone.utc).isoformat(),
        )
        if not record.task_id or not record.goal:
            raise ValueError("task_id and goal are required")
        with self._lock:
            self._records.append(record)
            self._records = self._records[-self.max_records:]
            self._save_locked()
        return record

    def recent(self, limit: int = 10) -> tuple[TaskMemory, ...]:
        with self._lock:
            return tuple(self._records[-max(0, limit):])

    def find(self, text: str, limit: int = 5) -> tuple[TaskMemory, ...]:
        terms = {x.lower() for x in text.split() if len(x) > 2}
        if not terms:
            return ()
        with self._lock:
            scored = []
            for record in self._records:
                haystack = f"{record.goal} {' '.join(record.results)}".lower()
                score = sum(term in haystack for term in terms)
                if score:
                    scored.append((score, record))
            scored.sort(key=lambda item: (item[0], item[1].timestamp), reverse=True)
            return tuple(record for _, record in scored[:max(0, limit)])

    def summary(self, text: str = "") -> dict[str, Any]:
        matches = self.find(text) if text.strip() else self.recent(5)
        return {"count": len(self._records), "matches": [asdict(item) for item in matches]}

    def _load(self) -> None:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                self._records = [
                    TaskMemory(str(x["task_id"]), str(x["goal"]), str(x["status"]),
                               tuple(x.get("results", ())), str(x.get("error", "")), str(x["timestamp"]))
                    for x in data[-self.max_records:] if isinstance(x, dict) and "task_id" in x and "goal" in x
                ]
        except (OSError, ValueError, TypeError, KeyError):
            self._records = []

    def _save_locked(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        temp.write_text(json.dumps([asdict(x) for x in self._records], ensure_ascii=False, indent=2), encoding="utf-8")
        temp.replace(self.path)
