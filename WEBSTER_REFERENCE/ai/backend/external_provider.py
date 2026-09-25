"""Optional external provider boundary; disabled by default and never stores API keys."""
from __future__ import annotations
class ExternalProvider:
    name="external-optional"
    def __init__(self,base_url=None): self.base_url=base_url
    def available(self): return bool(self.base_url)
    def generate(self,prompt): raise RuntimeError("external provider is not enabled in the local-first build")
