"""Local model selection and routing."""
from __future__ import annotations
class ModelRouter:
    def choose(self,models,requested=None):
        if requested:
            for m in models:
                if m.model_id==requested:return m
        models=list(models)
        if not models: raise RuntimeError("no local model registered")
        return next((m for m in models if m.format=="gguf"),models[0])
