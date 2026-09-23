from WEBSTER_REFERENCE.desktop.desktop_runtime import DesktopRuntime
from WEBSTER_REFERENCE.desktop.keyboard_driver import KeyboardDriver
from WEBSTER_REFERENCE.desktop.process_discovery import ProcessDiscovery
from WEBSTER_REFERENCE.desktop.system_interface import SystemInterface


def test_system_snapshot_is_observable() -> None:
    snapshot = SystemInterface().snapshot()
    assert snapshot.platform
    assert snapshot.python
    assert snapshot.cpu_count >= 1


def test_process_discovery_is_bounded() -> None:
    rows = ProcessDiscovery().list(limit=3)
    assert len(rows) <= 3
    assert all(row.pid > 0 and row.name for row in rows)


def test_desktop_aliases_are_explicit() -> None:
    runtime = DesktopRuntime()
    assert runtime.APP_ALIASES["notepad"] == "notepad.exe"
    assert runtime.APP_ALIASES["calculator"] == "calc.exe"


def test_keyboard_driver_rejects_unknown_key_without_injection() -> None:
    driver = KeyboardDriver()
    try:
        driver._vk("not-a-real-key")
    except ValueError:
        return
    raise AssertionError("unknown key should be rejected")


def test_unknown_desktop_request_is_not_handled() -> None:
    result = DesktopRuntime().handle("tell me a joke")
    assert not result.handled
