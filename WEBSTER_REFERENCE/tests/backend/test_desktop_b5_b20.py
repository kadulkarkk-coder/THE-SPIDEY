from WEBSTER_REFERENCE.desktop.mouse_driver import MouseDriver
from WEBSTER_REFERENCE.desktop.file_operations import FileOperations
from WEBSTER_REFERENCE.desktop.desktop_controller import DesktopController
from WEBSTER_REFERENCE.desktop.safe_shell import SafeShell
from WEBSTER_REFERENCE.desktop.desktop_permissions import DesktopPermissions

def test_mouse_driver_exists():
    assert MouseDriver().LEFT == 2

def test_file_operations_allow_text_only():
    assert ".py" in FileOperations.ALLOWED
    assert ".exe" not in FileOperations.ALLOWED

def test_shell_is_allowlisted():
    try:
        SafeShell().run("del everything")
    except PermissionError:
        return
    raise AssertionError("non-allowlisted shell action must be rejected")

def test_permissions_require_approval_for_write():
    policy=DesktopPermissions()
    assert policy.allowed("local","desktop.system.read")
    assert not policy.allowed("local","desktop.mouse.write")
    assert policy.allowed("local","desktop.mouse.write",approved=True)

def test_controller_is_unified():
    controller=DesktopController()
    assert controller.runtime is not None
    assert controller.audit is not None
