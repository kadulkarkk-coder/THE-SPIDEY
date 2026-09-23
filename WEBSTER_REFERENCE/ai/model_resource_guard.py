"""Per-request resource guard; no continuous polling."""
from __future__ import annotations
import time
class ModelResourceGuard:
    def __init__(self,max_seconds=30,max_tokens=512): self.max_seconds=max_seconds; self.max_tokens=max_tokens
    def validate(self,max_tokens):
        if max_tokens<1 or max_tokens>self.max_tokens: raise ValueError("token budget exceeds local resource policy")
    def timed(self,fn,*args,**kwargs):
        started=time.perf_counter(); out=fn(*args,**kwargs); elapsed=time.perf_counter()-started
        if elapsed>self.max_seconds: raise TimeoutError("local inference exceeded resource policy")
        return out
