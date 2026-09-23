"""B7 clipboard read/write boundary."""
from __future__ import annotations
import ctypes, os
class ClipboardControl:
    def __init__(self): self.user32=ctypes.windll.user32 if os.name=="nt" else None
    def _req(self):
        if self.user32 is None: raise OSError("Clipboard control is currently implemented for Windows.")
    def get(self):
        self._req()
        if not self.user32.OpenClipboard(0): raise RuntimeError("Could not open clipboard.")
        try:
            h=self.user32.GetClipboardData(13)
            if not h: return ""
            k=ctypes.windll.kernel32; p=k.GlobalLock(h)
            if not p: return ""
            try: return ctypes.wstring_at(p)
            finally: k.GlobalUnlock(h)
        finally: self.user32.CloseClipboard()
    def set(self,text):
        self._req(); value=text[:5000]
        if not self.user32.OpenClipboard(0): raise RuntimeError("Could not open clipboard.")
        try:
            self.user32.EmptyClipboard(); k=ctypes.windll.kernel32
            data=ctypes.create_unicode_buffer(value); k.GlobalAlloc.restype=ctypes.c_void_p
            h=k.GlobalAlloc(0x42,ctypes.sizeof(data)); p=k.GlobalLock(h); ctypes.memmove(p,ctypes.addressof(data),ctypes.sizeof(data)); k.GlobalUnlock(h)
            if not self.user32.SetClipboardData(13,h): raise RuntimeError("Clipboard write failed.")
        finally: self.user32.CloseClipboard()
        return f"Copied {len(value)} characters"