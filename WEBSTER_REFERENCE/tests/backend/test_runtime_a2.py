"""A2 tests for the single runtime request boundary."""
from __future__ import annotations

from WEBSTER_REFERENCE.core.application import WebsterApplication
from WEBSTER_REFERENCE.core.command_contracts import CommandRequest
from WEBSTER_REFERENCE.runtime.runtime_manager import RuntimeManager
from WEBSTER_REFERENCE.runtime.request_bridge import RuntimeRequestBridge


def test_bridge_rejects_requests_before_runtime_start() -> None:
    app = WebsterApplication()
    response = app.handle(CommandRequest("help"))
    assert response.ok is False
    assert response.error_code == "RUNTIME_NOT_RUNNING"


def test_bridge_dispatches_after_start() -> None:
    app = WebsterApplication()
    app.start()
    try:
        response = app.handle(CommandRequest("help"))
        assert response.ok is True
        assert "Available commands" in response.message
        assert app.runtime.snapshot().request_count == 1
    finally:
        app.stop()


def test_bridge_converts_unexpected_pipeline_failure() -> None:
    runtime = RuntimeManager()
    runtime.start()

    class BrokenPipeline:
        def process(self, request):
            raise RuntimeError("boom")

    bridge = RuntimeRequestBridge(BrokenPipeline(), runtime)
    response = bridge.submit(CommandRequest("test"))
    assert response.ok is False
    assert response.error_code == "INTERNAL_RUNTIME_ERROR"
    assert runtime.snapshot().failure_count == 1
    runtime.stop()
