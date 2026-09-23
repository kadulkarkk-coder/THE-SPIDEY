"""Deterministic semantic adapter for intent/entity hints; optional model hook."""
from __future__ import annotations
class SemanticAdapter:
    def classify(self,text):
        t=" ".join((text or "").lower().split())
        intent="question" if t.endswith("?") else "command" if t.startswith(("open ","launch ","run ","click ","type ")) else "statement"
        domain="desktop" if any(x in t for x in ("window","mouse","keyboard","clipboard","screen","file","browser")) else "general"
        return {"intent":intent,"domain":domain,"keywords":tuple(t.split()[:12])}
