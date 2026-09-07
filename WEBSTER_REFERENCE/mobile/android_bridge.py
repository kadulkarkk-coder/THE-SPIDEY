"""Small Android bridge used by the Chaquopy client."""
from __future__ import annotations

from core.application import WebsterApplication

_app: WebsterApplication | None = None


def bootstrap() -> dict[str, object]:
    global _app
    if _app is None:
        _app = WebsterApplication()
        _app.start()
    return _app.status()


def command(text: str) -> str:
    if _app is None:
        bootstrap()
    assert _app is not None
    return str(_app.command(text))


def shutdown() -> None:
    global _app
    if _app is not None:
        _app.stop()
        _app = None
