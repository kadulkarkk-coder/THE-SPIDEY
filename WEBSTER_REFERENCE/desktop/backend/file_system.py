"""Permission-aware filesystem operations using a configured root."""
from __future__ import annotations
from pathlib import Path

class FileSystem:
    def __init__(self, root: str | Path = ".") -> None: self.root = Path(root).resolve()
    def resolve(self, path: str | Path) -> Path:
        candidate = (self.root / path).resolve()
        if candidate != self.root and self.root not in candidate.parents: raise PermissionError("path escapes filesystem root")
        return candidate
    def exists(self, path: str | Path) -> bool: return self.resolve(path).exists()
    def read_text(self, path: str | Path, *, max_chars: int = 1_000_000) -> str:
        if max_chars < 1: raise ValueError("max_chars must be positive")
        return self.resolve(path).read_text(encoding="utf-8")[:max_chars]
    def write_text(self, path: str | Path, text: str, *, authorized: bool = False) -> Path:
        if not authorized: raise PermissionError("filesystem writes require explicit authorization")
        target = self.resolve(path); target.parent.mkdir(parents=True, exist_ok=True); target.write_text(text, encoding="utf-8"); return target
    def list(self, path: str | Path = ".") -> tuple[str, ...]: return tuple(sorted(p.name for p in self.resolve(path).iterdir()))
