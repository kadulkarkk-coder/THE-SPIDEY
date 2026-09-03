"""Thread-safe registry for approved WEBSTER tools."""
from __future__ import annotations
from threading import RLock
from .tool_contract import ToolBinding

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolBinding] = {}
        self._lock = RLock()

    def register(self, binding: ToolBinding) -> None:
        name = binding.spec.normalized_name()
        if not name or not callable(binding.handler):
            raise ValueError("valid tool name and callable handler are required")
        with self._lock:
            self._tools[name] = binding

    def get(self, name: str) -> ToolBinding | None:
        with self._lock:
            return self._tools.get(name.strip().lower())

    def names(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(sorted(self._tools))

    def remove(self, name: str) -> bool:
        with self._lock:
            return self._tools.pop(name.strip().lower(), None) is not None
