"""Persistent bounded conversation memory for WEBSTER A9."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from threading import RLock

@dataclass(frozen=True)
class ConversationMemory:
    session_id: str
    role: str
    text: str
    timestamp: str

class ConversationMemoryStore:
    """Local bounded conversation history with relevance retrieval."""
    def __init__(self, path: str | Path | None = None, max_records: int = 500) -> None:
        if max_records < 1: raise ValueError("max_records must be positive")
        self.path = Path(path) if path else Path.home() / ".webster" / "conversation_memory.json"
        self.max_records = max_records
        self._lock = RLock()
        self._records: list[ConversationMemory] = []
        self._load()

    def remember(self, session_id: str, role: str, text: str) -> ConversationMemory:
        record = ConversationMemory(session_id.strip(), role.strip().lower(), " ".join(text.split())[:2000], datetime.now(timezone.utc).isoformat())
        if not record.session_id or not record.role or not record.text: raise ValueError("conversation fields are required")
        with self._lock:
            self._records.append(record)
            self._records = self._records[-self.max_records:]
            self._save_locked()
        return record

    def recent(self, session_id: str = "", limit: int = 12) -> tuple[ConversationMemory, ...]:
        with self._lock:
            records = [x for x in self._records if not session_id or x.session_id == session_id]
            return tuple(records[-max(0, limit):])

    def search(self, query: str, session_id: str = "", limit: int = 8) -> tuple[ConversationMemory, ...]:
        terms = {x.lower() for x in query.split() if len(x) > 2}
        if not terms: return ()
        with self._lock:
            scored = []
            for record in self._records:
                if session_id and record.session_id != session_id: continue
                score = sum(term in record.text.lower() for term in terms)
                if score: scored.append((score, record))
            scored.sort(key=lambda item: (item[0], item[1].timestamp), reverse=True)
            return tuple(item[1] for item in scored[:max(0, limit)])

    def context(self, query: str, session_id: str, limit: int = 8) -> str:
        return "\n".join(f"{m.role}: {m.text}" for m in self.search(query, session_id, limit))

    def _load(self) -> None:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                self._records = [ConversationMemory(str(x["session_id"]), str(x["role"]), str(x["text"]), str(x["timestamp"])) for x in data[-self.max_records:] if isinstance(x, dict) and all(k in x for k in ("session_id","role","text","timestamp"))]
        except (OSError, ValueError, TypeError, KeyError): self._records = []

    def _save_locked(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        temp.write_text(json.dumps([asdict(x) for x in self._records], ensure_ascii=False, indent=2), encoding="utf-8")
        temp.replace(self.path)
