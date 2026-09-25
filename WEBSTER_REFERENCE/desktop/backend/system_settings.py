"""B12 read-only system settings."""
import os, locale, platform
class SystemSettings:
    def snapshot(self):
        return {"os":platform.platform(),"computer":platform.node(),"language":locale.getdefaultlocale()[0] or "unknown","username":os.environ.get("USERNAME","")}