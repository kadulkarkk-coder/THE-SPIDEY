"""A1 runtime foundation tests."""
from __future__ import annotations

import unittest

from WEBSTER_REFERENCE.core.application import WebsterApplication
from WEBSTER_REFERENCE.runtime.runtime_manager import RuntimeManager
from WEBSTER_REFERENCE.runtime.runtime_state import RuntimeState


class RuntimeManagerTests(unittest.TestCase):
    def test_lifecycle_and_service_order(self) -> None:
        manager = RuntimeManager()
        events: list[str] = []
        manager.register_service("one", lambda: events.append("start-one"), lambda: events.append("stop-one"))
        manager.register_service("two", lambda: events.append("start-two"), lambda: events.append("stop-two"))
        manager.start()
        self.assertEqual(manager.state, RuntimeState.RUNNING)
        manager.stop()
        self.assertEqual(manager.state, RuntimeState.STOPPED)
        self.assertEqual(events, ["start-one", "start-two", "stop-two", "stop-one"])


class ApplicationRuntimeTests(unittest.TestCase):
    def test_application_starts_and_routes_status(self) -> None:
        app = WebsterApplication()
        app.start()
        try:
            self.assertTrue(app.status()["running"])
            response = app.handle(__import__("WEBSTER_REFERENCE.core.command_contracts", fromlist=["CommandRequest"]).CommandRequest("status"))
            self.assertTrue(response.ok)
            self.assertEqual(app.runtime.state, RuntimeState.RUNNING)
            self.assertEqual(app.runtime.request_count, 1)
        finally:
            app.stop()
        self.assertFalse(app.status()["running"])


if __name__ == "__main__":
    unittest.main()
