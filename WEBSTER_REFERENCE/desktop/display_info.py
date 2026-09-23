"""B11 display information."""
import ctypes, os
class DisplayInfo:
    def snapshot(self):
        if os.name!="nt": return {"platform":os.name}
        u=ctypes.windll.user32
        return {"width":u.GetSystemMetrics(0),"height":u.GetSystemMetrics(1),"work_width":u.GetSystemMetrics(78),"work_height":u.GetSystemMetrics(79)}