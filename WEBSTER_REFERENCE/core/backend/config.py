"""Minimal validated runtime configuration for WEBSTER."""
from __future__ import annotations
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class WebsterConfig:
    name: str = "WEBSTER"
    version: str = "0.1.0-alpha"
    environment: str = "development"
    debug: bool = False

    @classmethod
    def from_environment(cls) -> "WebsterConfig":
        raw = os.getenv("WEBSTER_DEBUG", "0").strip().lower()
        debug = raw in {"1", "true", "yes", "on"}
        environment = os.getenv("WEBSTER_ENV", "development").strip() or "development"
        return cls(environment=environment, debug=debug)
