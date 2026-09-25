"""B19 capability permission policy with principal grants."""
from __future__ import annotations
class DesktopPermissions:
    READ={"desktop.system.read","desktop.process.read","desktop.window.read","desktop.display.read","desktop.clipboard.read","desktop.shell.read"}
    def __init__(self): self._grants: dict[str,set[str]]={}
    def grant(self,principal,capability): self._grants.setdefault(principal.strip(),set()).add(capability.strip().lower())
    def revoke(self,principal,capability): self._grants.get(principal.strip(),set()).discard(capability.strip().lower())
    def allowed(self,principal,capability,approved=False):
        cap=capability.strip().lower()
        return cap in self.READ or approved or cap in self._grants.get(principal.strip(),set())
