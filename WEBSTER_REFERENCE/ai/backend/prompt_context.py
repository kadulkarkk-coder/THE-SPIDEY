"""Bounded prompt construction for local inference."""
from __future__ import annotations
class PromptContext:
    def __init__(self,max_chars=9000): self.max_chars=max_chars
    def build(self,system,user,history=(),evidence=()):
        parts=[system.strip()]
        for role,text in list(history)[-8:]: parts.append(f"{role}: {text}")
        if evidence: parts.append("Evidence:\n"+"\n".join(str(x) for x in list(evidence)[-6:]))
        parts.append("user: "+user.strip())
        return "\n".join(parts)[-self.max_chars:]
