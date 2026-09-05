"""Declarative manifest for WEBSTER's first desktop UI composition."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UIViewSpec:
    view_id: str
    title: str
    icon_asset: str | None = None


DEFAULT_VIEWS = (
    UIViewSpec("home", "Home", "home_icon"),
    UIViewSpec("chat", "Chat", "chat_icon"),
    UIViewSpec("browser", "Browser", "browser_icon"),
    UIViewSpec("memory", "Memory", "memory_icon"),
    UIViewSpec("automation", "Automation", "automation_icon"),
    UIViewSpec("settings", "Settings", "settings_icon"),
)
