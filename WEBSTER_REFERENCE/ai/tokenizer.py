"""Tokenizer abstraction with a dependency-free fallback."""
from __future__ import annotations
import re
class Tokenizer:
    def __init__(self): self._pattern=re.compile(r"\w+|[^\w\s]",re.UNICODE)
    def encode(self,text): return self._pattern.findall(text or "")
    def decode(self,tokens): return " ".join(tokens)
    def count(self,text): return len(self.encode(text))
    def truncate(self,text,max_tokens): return self.decode(self.encode(text)[:max_tokens])
