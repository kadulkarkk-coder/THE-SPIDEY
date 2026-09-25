"""Dependency-free hashed embedding boundary for local retrieval."""
from __future__ import annotations
import math
class EmbeddingAdapter:
    def __init__(self,dimensions=64): self.dimensions=dimensions
    def embed(self,text):
        v=[0.0]*self.dimensions
        for token in str(text).lower().split(): v[hash(token)%self.dimensions]+=1.0
        n=math.sqrt(sum(x*x for x in v)) or 1.0
        return tuple(x/n for x in v)
    def similarity(self,a,b): return sum(x*y for x,y in zip(a,b))
