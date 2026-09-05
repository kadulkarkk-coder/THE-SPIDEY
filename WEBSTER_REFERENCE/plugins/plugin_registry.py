"""Thread-safe plugin registration and capability discovery."""
from __future__ import annotations

from threading import RLock

from .plugin_types import PluginSpec


class PluginRegistry:
    """Index plugins by ID and capability without importing provider code."""

    def __init__(self) -> None:
        self._plugins: dict[str, PluginSpec] = {}
        self._lock = RLock()

    def register(self, plugin: PluginSpec) -> PluginSpec:
        with self._lock:
            if plugin.plugin_id in self._plugins:
                raise ValueError(f"plugin already registered: {plugin.plugin_id}")
            self._plugins[plugin.plugin_id] = plugin
        return plugin

    def get(self, plugin_id: str) -> PluginSpec:
        with self._lock:
            return self._plugins[plugin_id]

    def find_by_capability(self, capability: str) -> tuple[PluginSpec, ...]:
        capability = capability.strip()
        with self._lock:
            return tuple(plugin for plugin in self._plugins.values() if capability in plugin.capabilities)

    def list(self) -> tuple[PluginSpec, ...]:
        with self._lock:
            return tuple(self._plugins.values())
