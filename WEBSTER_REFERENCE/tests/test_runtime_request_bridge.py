"""A2 tests for the single runtime request boundary."""
from __future__ import annotations

from WEBSTER_REFERENCE.core.command_contracts import CommandRequest, CommandResponse
from WEBSTER_REFERENCE.runtime.request_bridge import RuntimeRequestBridge
from WEBSTER_REFERENCE.runtime.runtime_manager import RuntimeManager


class FakePipeline:
    def __init__(self, ok: bool = True) -> None:
        self.ok = ok

    def process(self, request: CommandRequest) -> CommandResponse:
        if self.ok:
            return CommandResponse.success(request, "handled")
        return CommandResponse.failure(request, "failed", "TEST_FAILURE")


def running_runtime() -> RuntimeManager:
    runtime = RuntimeManager()
    runtime.start()
    return runtime


def test_bridge_requires_running_runtime() -> None:
    runtime = RuntimeManager()
    bridge = RuntimeRequestBridge(FakePipeline(), runtime)
    response = bridge.submit(CommandRequest("hello"))
    assert not response.ok
    assert response.error_code == "RUNTIME_NOT_RUNNING"
    assert runtime.request_count == 1


def test_bridge_records_success() -> None:
    runtime = running_runtime()
    bridge = RuntimeRequestBridge(FakePipeline(), runtime)
    response = bridge.submit(CommandRequest("hello"))
    assert response.ok
    assert response.message == "handled"
    assert runtime.request_count == 1
    assert runtime.error_count == 0
    runtime.stop()


def test_bridge_records_failed_response() -> None:
    runtime = running_runtime()
    bridge = RuntimeRequestBridge(FakePipeline(ok=False), runtime)
    response = bridge.submit(CommandRequest("hello"))
    assert not response.ok
    assert response.error_code == "TEST_FAILURE"
    assert runtime.request_count == 1
    assert runtime.error_count == 1
    runtime.stop()


def test_bridge_contains_unexpected_pipeline_exception() -> None:
    class BrokenPipeline:
        def process(self, request: CommandRequest) -> CommandResponse:
            raise RuntimeError("boom")

    runtime = running_runtime()
    bridge = RuntimeRequestBridge(BrokenPipeline(), runtime)
    response = bridge.submit(CommandRequest("hello"))
    assert not response.ok
    assert response.error_code == "INTERNAL_RUNTIME_ERROR"
    assert runtime.request_count == 1
    assert runtime.error_count == 1
    runtime.stop()
