"""Lifecycle manager for built-in and optional WEBSTER plugins."""
from __future__ import annotations

from threading import RLock
from importlib import import_module
from types import ModuleType

from .builtin_plugins import BUILTIN_PLUGINS
from .plugin_types import PluginSpec, PluginState, PluginStatus


class PluginManager:
    """Register, toggle, and explicitly load plugin modules."""

    def __init__(self, plugins: tuple[PluginSpec, ...] = BUILTIN_PLUGINS) -> None:
        self._plugins: dict[str, PluginSpec] = {}
        self._states: dict[str, PluginState] = {}
        self._modules: dict[str, ModuleType] = {}
        self._lock = RLock()
        for plugin in plugins:
            self.register(plugin, enabled=plugin.builtin)

    def register(self, plugin: PluginSpec, *, enabled: bool = False) -> PluginSpec:
        with self._lock:
            if plugin.plugin_id in self._plugins:
                raise ValueError(f"plugin already registered: {plugin.plugin_id}")
            self._plugins[plugin.plugin_id] = plugin
            self._states[plugin.plugin_id] = PluginState(
                plugin.plugin_id,
                PluginStatus.ENABLED if enabled else PluginStatus.DISABLED,
                "enabled" if enabled else "disabled",
            )
        return plugin

    def enable(self, plugin_id: str) -> PluginState:
        return self._set_status(plugin_id, PluginStatus.ENABLED, "enabled")

    def disable(self, plugin_id: str) -> PluginState:
        with self._lock:
            self._modules.pop(plugin_id, None)
        return self._set_status(plugin_id, PluginStatus.DISABLED, "disabled")

    def load(self, plugin_id: str) -> ModuleType:
        """Load a declared module only when explicitly requested."""
        with self._lock:
            spec = self._plugins[plugin_id]
            if self._states[plugin_id].status != PluginStatus.ENABLED:
                raise RuntimeError(f"plugin is not enabled: {plugin_id}")
            module_name = spec.metadata.get("module", "").strip()
            if not module_name:
                raise ValueError(f"plugin has no module: {plugin_id}")
            module = import_module(module_name)
            self._modules[plugin_id] = module
            return module

    def unload(self, plugin_id: str) -> None:
        with self._lock:
            self._modules.pop(plugin_id, None)

    def _set_status(self, plugin_id: str, status: PluginStatus, message: str) -> PluginState:
        with self._lock:
            if plugin_id not in self._plugins:
                raise KeyError(plugin_id)
            state = PluginState(plugin_id, status, message)
            self._states[plugin_id] = state
            return state

    def get(self, plugin_id: str) -> PluginSpec:
        with self._lock:
            return self._plugins[plugin_id]

    def state(self, plugin_id: str) -> PluginState:
        with self._lock:
            return self._states[plugin_id]

    def list(self) -> tuple[PluginSpec, ...]:
        with self._lock:
            return tuple(self._plugins.values())

    def enabled(self) -> tuple[PluginSpec, ...]:
        with self._lock:
            return tuple(self._plugins[item] for item, state in self._states.items() if state.status == PluginStatus.ENABLED)

    def loaded(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(self._modules)
