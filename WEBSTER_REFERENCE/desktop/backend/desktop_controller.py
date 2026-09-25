"""B20 unified desktop controller."""
from __future__ import annotations
from .desktop_runtime import DesktopRuntime,DesktopAction
from .mouse_driver import MouseDriver
from .clipboard_control import ClipboardControl
from .display_info import DisplayInfo
from .file_operations import FileOperations
from .window_actions import WindowActions
from .notification_control import NotificationControl
from .desktop_automation import DesktopAutomation
from .system_settings import SystemSettings
from .safe_shell import SafeShell
from .browser_control import BrowserControl
from .screenshot_control import ScreenshotControl
from .hotkey_manager import HotkeyManager
from .desktop_audit import DesktopAuditTrail
from .desktop_permissions import DesktopPermissions
class DesktopController:
    def __init__(self):
        self.runtime=DesktopRuntime(); self.files=FileOperations(); self.windows=WindowActions(); self.notifications=NotificationControl(); self.mouse=MouseDriver(); self.clipboard=ClipboardControl(); self.display=DisplayInfo(); self.settings=SystemSettings(); self.shell=SafeShell(); self.browser=BrowserControl(); self.screenshot=ScreenshotControl(); self.hotkeys=HotkeyManager(); self.audit=DesktopAuditTrail(); self.permissions=DesktopPermissions(); self.automation=DesktopAutomation(self)
    def execute(self,text,principal="local",approved=False):
        r=self.runtime.handle(text)
        if r.handled: self.audit.record(text,r.capability,r.ok,r.message); return r
        s=" ".join(text.strip().split()); low=s.casefold()
        try:
            if low in {"mouse position","cursor position"}:
                p=self.mouse.position(); r=DesktopAction(True,True,str(p),"desktop.mouse.read",{"position":p})
            elif low.startswith("move mouse to "):
                x,y=map(int,low.removeprefix("move mouse to ").split(",",1)); ok=self.permissions.allowed(principal,"desktop.mouse.write",approved); r=DesktopAction(True,ok,"Mouse movement requires approval" if not ok else self.mouse.move(x,y),"desktop.mouse.write")
            elif low.startswith("click ") or low.startswith("double click "):
                double=low.startswith("double click "); button=s.split()[-1].lower(); ok=self.permissions.allowed(principal,"desktop.mouse.write",approved); r=DesktopAction(True,ok,"Mouse click requires approval" if not ok else self.mouse.click(button,double),"desktop.mouse.write")
            elif low.startswith("scroll "):
                n=int(low.split()[-1]); ok=self.permissions.allowed(principal,"desktop.mouse.write",approved); r=DesktopAction(True,ok,"Mouse scroll requires approval" if not ok else self.mouse.scroll(n),"desktop.mouse.write")
            elif low in {"get clipboard","read clipboard"}: r=DesktopAction(True,True,self.clipboard.get(),"desktop.clipboard.read")
            elif low.startswith("set clipboard ") or low.startswith("copy "):
                value=s.split(" ",2)[2]; ok=self.permissions.allowed(principal,"desktop.clipboard.write",approved); r=DesktopAction(True,ok,"Clipboard write requires approval" if not ok else self.clipboard.set(value),"desktop.clipboard.write")
            elif low.startswith("search web "): r=DesktopAction(True,True,self.browser.search(s[11:]),"desktop.browser.open")
            elif low.startswith("shell "): r=DesktopAction(True,True,self.shell.run(s[6:]),"desktop.shell.read")
            elif low=="display info": r=DesktopAction(True,True,str(self.display.snapshot()),"desktop.display.read")
            elif low=="settings info": r=DesktopAction(True,True,str(self.settings.snapshot()),"desktop.settings.read")
            elif low.startswith("list files"):
                path=s[10:].strip() or "."; r=DesktopAction(True,True,str(self.files.list_dir(path)),"desktop.file.read")
            elif low.startswith("read file "):
                r=DesktopAction(True,True,self.files.read(s[10:].strip()),"desktop.file.read")
            elif low.startswith("focus window "):
                r=DesktopAction(True,True,self.windows.focus(s[13:].strip()),"desktop.window.write")
            elif low.startswith("minimize window "):
                r=DesktopAction(True,True,self.windows.minimize(s[16:].strip()),"desktop.window.write")
            elif low.startswith("maximize window "):
                r=DesktopAction(True,True,self.windows.maximize(s[16:].strip()),"desktop.window.write")
            elif low.startswith("restore window "):
                r=DesktopAction(True,True,self.windows.restore(s[15:].strip()),"desktop.window.write")
            elif low.startswith("notify "):
                value=s[7:].strip(); parts=value.split(":",1); title=parts[0].strip() if len(parts)>1 else "WEBSTER"; message=parts[1].strip() if len(parts)>1 else value; r=DesktopAction(True,True,self.notifications.notify(title,message),"desktop.notification.write")
            elif low.startswith("do sequence "):
                ok,out=self.automation.run(s[12:].strip(),approved=approved); r=DesktopAction(True,ok," | ".join(out),"desktop.automation")
            elif low.startswith("screenshot "):
                ok=self.permissions.allowed(principal,"desktop.file.write",approved); r=DesktopAction(True,ok,"Screenshot requires approval" if not ok else self.screenshot.capture(s[11:]),"desktop.file.write")
            elif low.startswith("hotkey "):
                ok=self.permissions.allowed(principal,"desktop.keyboard.write",approved); r=DesktopAction(True,ok,"Hotkey requires approval" if not ok else self.hotkeys.execute(s[7:]),"desktop.keyboard.write")
            else: return DesktopAction(False,True,"")
        except Exception as exc: r=DesktopAction(True,False,str(exc))
        self.audit.record(text,r.capability,r.ok,r.message); return r
