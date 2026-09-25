"""B18 bounded desktop audit trail."""
from dataclasses import dataclass
from collections import deque
from time import time
@dataclass(frozen=True)
class DesktopAudit:
    action:str; capability:str; ok:bool; message:str; timestamp:float
class DesktopAuditTrail:
    def __init__(self,max_items=200): self.items=deque(maxlen=max_items)
    def record(self,action,capability,ok,message): self.items.append(DesktopAudit(action,capability,ok,message,time()))
    def recent(self,limit=20): return tuple(list(self.items)[-max(1,min(limit,50)):])