"""B10 window state actions."""
from .window_control import WindowController
class WindowActions:
    def __init__(self): self.windows=WindowController()
    def focus(self,h): return self.windows.focus(int(h))
    def minimize(self,h): return self.windows.minimize(int(h))
    def maximize(self,h): return self.windows.maximize(int(h))
    def restore(self,h): return self.windows.restore(int(h))