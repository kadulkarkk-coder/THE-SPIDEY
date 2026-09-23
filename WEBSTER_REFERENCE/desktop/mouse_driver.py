"""B6 real Windows mouse input boundary."""
from __future__ import annotations
import ctypes, os, time
from ctypes import wintypes
class MouseDriver:
    LEFT=2; LEFT_UP=4; RIGHT=8; RIGHT_UP=16; MIDDLE=32; MIDDLE_UP=64; WHEEL=2048
    def __init__(self): self.user32=ctypes.windll.user32 if os.name=="nt" else None
    def _req(self):
        if self.user32 is None: raise OSError("Mouse control is currently implemented for Windows.")
    def position(self):
        self._req(); p=wintypes.POINT(); self.user32.GetCursorPos(ctypes.byref(p)); return p.x,p.y
    def move(self,x,y):
        self._req(); x=int(x); y=int(y)
        if not (0<=x<=10000 and 0<=y<=10000): raise ValueError("Mouse coordinates out of safe range.")
        self.user32.SetCursorPos(x,y); return f"Moved mouse to {x}, {y}"
    def click(self,button="left",double=False):
        self._req(); flags={"left":(2,4),"right":(8,16),"middle":(32,64)}
        if button not in flags: raise ValueError("Unsupported mouse button.")
        down,up=flags[button]
        for _ in range(2 if double else 1): self.user32.mouse_event(down,0,0,0,0); self.user32.mouse_event(up,0,0,0,0); time.sleep(.04)
        return f"{'Double-clicked' if double else 'Clicked'} {button}"
    def scroll(self,clicks):
        self._req(); n=max(-20,min(20,int(clicks))); self.user32.mouse_event(2048,0,0,n*120,0); return f"Scrolled {n}"