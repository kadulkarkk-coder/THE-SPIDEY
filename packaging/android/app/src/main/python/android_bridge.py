"""Android bridge for the lightweight WEBSTER Mark D runtime."""
from __future__ import annotations

from WEBSTER_REFERENCE.core.application import WebsterApplication

_app: WebsterApplication | None = None


def bootstrap() -> str:
    """Start the shared WEBSTER core once and return a compact status message."""
    global _app
    if _app is None:
        _app = WebsterApplication()
    _app.start()
    status = _app.status()
    return f"{status['name']} {status['version']} | offline={status['healthy']}"


def command(text: str) -> str:
    """Run one text command through the shared WEBSTER core."""
    if _app is None:
        bootstrap()
    assert _app is not None
    return _app.command(text)
