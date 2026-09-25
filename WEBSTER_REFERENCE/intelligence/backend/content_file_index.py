"""Local content-aware file indexing and search for WEBSTER A14.

The index is intentionally local-first and bounded. It reads text files from
explicitly approved roots in a low-priority background worker, stores compact
content metadata, and ranks matches from file contents rather than filenames.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import os
import re
import threading
from time import monotonic
from typing import Iterable


DEFAULT_EXTENSIONS = frozenset({
    ".txt", ".md", ".rst", ".log", ".csv", ".json", ".yaml", ".yml",
    ".ini", ".cfg", ".conf", ".py", ".js", ".ts", ".tsx", ".jsx",
    ".java", ".c", ".h", ".cpp", ".hpp", ".cs", ".go", ".rs", ".html",
    ".htm", ".css", ".scss", ".sql", ".xml",
})


@dataclass(frozen=True)
class FileContentRecord:
    path: str
    content_hash: str
    size: int
    modified_ns: int
    terms: frozenset[str]
    excerpt: str = ""


@dataclass(frozen=True)
class FileSearchResult:
    path: str
    score: float
    matched_terms: tuple[str, ...]
    excerpt: str
    indexed_at: float

    def as_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "score": round(self.score, 4),
            "matched_terms": list(self.matched_terms),
            "excerpt": self.excerpt,
            "indexed_at": self.indexed_at,
        }


class ContentFileIndex:
    """Bounded content index with an optional low-priority background refresh."""

    def __init__(
        self,
        roots: Iterable[str | Path] = (),
        *,
        max_files: int = 2000,
        max_file_bytes: int = 2_000_000,
        max_excerpt_chars: int = 280,
        extensions: frozenset[str] = DEFAULT_EXTENSIONS,
    ) -> None:
        self.max_files = max(1, max_files)
        self.max_file_bytes = max(1_000, max_file_bytes)
        self.max_excerpt_chars = max(80, max_excerpt_chars)
        self.extensions = frozenset(ext.lower() for ext in extensions)
        self._roots: list[Path] = []
        self._records: dict[str, FileContentRecord] = {}
        self._lock = threading.RLock()
        self._stop = threading.Event()
        self._worker: threading.Thread | None = None
        self.set_roots(roots)

    @classmethod
    def from_environment(cls) -> "ContentFileIndex":
        raw = os.environ.get("WEBSTER_FILE_ROOTS", "")
        roots = [item.strip() for item in raw.split(os.pathsep) if item.strip()]
        return cls(roots)

    def set_roots(self, roots: Iterable[str | Path]) -> None:
        normalized: list[Path] = []
        for root in roots:
            path = Path(root).expanduser()
            try:
                resolved = path.resolve()
            except OSError:
                continue
            if resolved.exists() and resolved.is_dir():
                normalized.append(resolved)
        with self._lock:
            self._roots = list(dict.fromkeys(normalized))

    def add_root(self, root: str | Path) -> bool:
        path = Path(root).expanduser()
        try:
            resolved = path.resolve()
        except OSError:
            return False
        if not resolved.exists() or not resolved.is_dir():
            return False
        with self._lock:
            if resolved not in self._roots:
                self._roots.append(resolved)
        return True

    def roots(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(str(root) for root in self._roots)

    def start_background_refresh(self) -> None:
        with self._lock:
            if self._worker and self._worker.is_alive():
                return
            self._stop.clear()
            self._worker = threading.Thread(
                target=self._refresh_worker,
                name="webster-file-index",
                daemon=True,
            )
            self._worker.start()

    def stop_background_refresh(self, timeout: float = 1.0) -> None:
        self._stop.set()
        worker = self._worker
        if worker and worker.is_alive():
            worker.join(timeout=max(0.1, timeout))
        self._worker = None

    def refresh(self, *, limit: int | None = None) -> int:
        with self._lock:
            roots = tuple(self._roots)
            current = dict(self._records)
        max_scan = max(1, limit or self.max_files)
        seen: set[str] = set()
        indexed = 0

        for root in roots:
            if self._stop.is_set():
                break
            try:
                iterator = root.rglob("*")
                for path in iterator:
                    if self._stop.is_set() or indexed >= max_scan:
                        break
                    if not path.is_file() or path.suffix.lower() not in self.extensions:
                        continue
                    try:
                        stat = path.stat()
                    except OSError:
                        continue
                    if stat.st_size > self.max_file_bytes:
                        continue
                    key = str(path)
                    seen.add(key)
                    old = current.get(key)
                    if old and old.modified_ns == stat.st_mtime_ns and old.size == stat.st_size:
                        indexed += 1
                        continue
                    record = self._read_record(path, stat.st_size, stat.st_mtime_ns)
                    if record:
                        current[key] = record
                        indexed += 1
                if indexed >= max_scan:
                    break
            except OSError:
                continue

        with self._lock:
            # Remove files that no longer exist only for paths inside approved roots.
            approved = tuple(self._roots)
            stale = [
                key for key in current
                if any(self._under_root(Path(key), root) for root in approved) and key not in seen
            ]
            for key in stale:
                current.pop(key, None)
            self._records = dict(list(current.items())[-self.max_files :])
        return indexed

    def search(self, query: str, *, limit: int = 5) -> tuple[FileSearchResult, ...]:
        terms = self._terms(query)
        if not terms:
            return ()
        with self._lock:
            records = tuple(self._records.values())
        scored: list[tuple[float, FileContentRecord, tuple[str, ...]]] = []
        for record in records:
            matches = tuple(sorted(term for term in terms if term in record.terms))
            if not matches:
                continue
            # Content evidence dominates. Filename is deliberately excluded from ranking.
            density = len(matches) / max(1, len(terms))
            score = density + min(0.35, len(matches) * 0.03)
            scored.append((score, record, matches))
        scored.sort(key=lambda item: (-item[0], item[1].path))
        now = monotonic()
        return tuple(
            FileSearchResult(record.path, score, matches, record.excerpt, now)
            for score, record, matches in scored[: max(1, limit)]
        )

    def indexed_count(self) -> int:
        with self._lock:
            return len(self._records)

    def status(self) -> dict[str, object]:
        return {"roots": list(self.roots()), "indexed_files": self.indexed_count(), "background": bool(self._worker and self._worker.is_alive())}

    def _refresh_worker(self) -> None:
        # One bounded pass avoids permanent polling and keeps laptop resource usage low.
        self.refresh()

    def _read_record(self, path: Path, size: int, modified_ns: int) -> FileContentRecord | None:
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8", errors="replace")
        except (OSError, UnicodeError):
            return None
        terms = frozenset(self._terms(text))
        digest = sha256(raw).hexdigest()
        excerpt = self._make_excerpt(text)
        return FileContentRecord(str(path), digest, size, modified_ns, terms, excerpt)

    @staticmethod
    def _terms(text: str) -> set[str]:
        return {
            token for token in re.findall(r"[a-zA-Z0-9_]{3,}", text.lower())
            if not token.isdigit()
        }

    def _make_excerpt(self, text: str) -> str:
        cleaned = " ".join(text.split())
        return cleaned[: self.max_excerpt_chars]

    @staticmethod
    def _under_root(path: Path, root: Path) -> bool:
        try:
            path.resolve().relative_to(root.resolve())
            return True
        except ValueError:
            return False
