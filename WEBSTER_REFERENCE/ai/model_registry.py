"""Bounded local model registry; no model is downloaded automatically."""
from __future__ import annotations
from .model_contracts import ModelDescriptor

class ModelRegistry:
    def __init__(self): self._models={}
    def register(self, descriptor: ModelDescriptor):
        if not descriptor.model_id.strip(): raise ValueError("model_id required")
        self._models[descriptor.model_id]=descriptor; return descriptor
    def get(self, model_id: str): return self._models.get(model_id)
    def list(self): return tuple(self._models.values())
    def remove(self, model_id: str): self._models.pop(model_id,None)
