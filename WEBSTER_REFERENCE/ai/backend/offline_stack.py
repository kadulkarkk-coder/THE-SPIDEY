"""Offline fallback stack: semantic hints, calculator-like responses and deterministic generation."""
from __future__ import annotations
from .semantic_adapter import SemanticAdapter
from .embedding_adapter import EmbeddingAdapter
class OfflineStack:
    def __init__(self): self.semantic=SemanticAdapter(); self.embedding=EmbeddingAdapter()
    def respond(self,prompt):
        info=self.semantic.classify(prompt)
        return f"Offline WEBSTER: {info['intent']} request in {info['domain']} domain."
