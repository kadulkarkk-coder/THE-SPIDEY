"""Inference abstraction; deterministic locally, optional GGUF when installed."""
from __future__ import annotations
import time
from .model_contracts import GenerationRequest,GenerationResponse,ModelDescriptor
from .tokenizer import Tokenizer

class InferenceEngine:
    def __init__(self,tokenizer=None): self.tokenizer=tokenizer or Tokenizer(); self._loaded={}
    def attach(self,descriptor:ModelDescriptor,backend): self._loaded[descriptor.model_id]=(descriptor,backend)
    def generate(self,request:GenerationRequest,descriptor:ModelDescriptor)->GenerationResponse:
        started=time.perf_counter(); item=self._loaded.get(descriptor.model_id)
        if item and item[1] is not None:
            out=item[1](request.prompt,max_tokens=request.max_tokens,temperature=request.temperature)
            text=out.get("choices",[{}])[0].get("text","").strip()
            return GenerationResponse(text,descriptor.model_id,"llama.cpp",self.tokenizer.count(text),(time.perf_counter()-started)*1000,0.7)
        text=self._deterministic(request.prompt)
        return GenerationResponse(text,descriptor.model_id,"local",self.tokenizer.count(text),(time.perf_counter()-started)*1000,0.65,(("mode","deterministic"),))
    @staticmethod
    def _deterministic(prompt):
        p=" ".join((prompt or "").split())
        if not p:return "Tell me what you need."
        return "Local model runtime received: " + p[:1200]
