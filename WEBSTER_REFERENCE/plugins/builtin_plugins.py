"""Safe, useful plugins enabled by default in WEBSTER Mark D."""
from __future__ import annotations

from .plugin_types import PluginSpec


BUILTIN_PLUGINS: tuple[PluginSpec, ...] = (
    PluginSpec("clock", "Clock", "Read local date, time, and timezone information.", ("time.read",), True),
    PluginSpec("notes", "Notes", "Create, update, search, and organize local notes.", ("notes.read", "notes.write"), True),
    PluginSpec("tasks", "Tasks", "Manage lightweight local tasks and completion state.", ("tasks.read", "tasks.write"), True),
    PluginSpec("calculator", "Calculator", "Perform deterministic arithmetic without network access.", ("math.calculate",), True),
    PluginSpec("system_status", "System Status", "Report safe local CPU, memory, battery, and runtime status.", ("system.status",), True),
    PluginSpec("file_search", "File Search", "Search user-approved local folders without modifying files.", ("files.search",), True),
    PluginSpec("clipboard", "Clipboard", "Read or write clipboard text only when explicitly permitted.", ("clipboard.read", "clipboard.write"), True),
    PluginSpec("weather", "Weather", "Provide weather through an optional network provider.", ("weather.read",), True, True),
    PluginSpec("web_search", "Web Search", "Search the web through an explicitly configured provider.", ("web.search",), True, True),
    PluginSpec("calendar", "Calendar", "Read and manage calendar events through a configured calendar provider.", ("calendar.read", "calendar.write"), True),
)


def builtin_plugin_ids() -> tuple[str, ...]:
    return tuple(plugin.plugin_id for plugin in BUILTIN_PLUGINS)
