"""B15 on-demand screenshot boundary."""
import os
class ScreenshotControl:
    def capture(self,path):
        try: from PIL import ImageGrab
        except ImportError as exc: raise RuntimeError("Screenshot support requires Pillow.") from exc
        target=os.path.abspath(path); ImageGrab.grab().save(target); return target