"""Spider-inspired theme presets for WEBSTER UI."""
from __future__ import annotations

from .ui_types import UITheme


SPIDER_THEME = UITheme(
    name="webster-spider",
    background="#08090d",
    foreground="#f5f5f7",
    accent="#e21b2d",
    surface="#14161c",
    metadata={"secondary_accent": "#b8bcc6", "web_glow": "#7f1822"},
)

LIGHT_THEME = UITheme(
    name="webster-light",
    background="#eef1f5",
    foreground="#17191f",
    accent="#b51224",
    surface="#ffffff",
)


class UIThemeCatalog:
    """Small immutable-by-convention collection of supported themes."""

    def __init__(self) -> None:
        self._themes = {theme.name: theme for theme in (SPIDER_THEME, LIGHT_THEME)}

    def get(self, name: str) -> UITheme:
        try:
            return self._themes[name.strip().lower()]
        except KeyError as exc:
            raise KeyError(f"unknown UI theme: {name}") from exc

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._themes))
