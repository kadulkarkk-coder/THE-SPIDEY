"""Unified C1-C20 local AI controller."""
from __future__ import annotations
from .model_contracts import ModelDescriptor
from .model_registry import ModelRegistry
from .model_loader import ModelLoader
from .inference_engine import InferenceEngine
from .local_generator import LocalGenerator
from .offline_stack import OfflineStack
from .model_router import ModelRouter
from .model_permissions import ModelPermissions
from .model_resource_guard import ModelResourceGuard
from .model_cache import ModelCache
from .learning_hooks import LearningHooks
from .model_benchmark import ModelBenchmark

class LocalAIController:
    def __init__(self):
        self.registry=ModelRegistry(); self.loader=ModelLoader(); self.engine=InferenceEngine(); self.generator=LocalGenerator(self.engine)
        self.offline=OfflineStack(); self.router=ModelRouter(); self.permissions=ModelPermissions(); self.guard=ModelResourceGuard(); self.cache=ModelCache(); self.learning=LearningHooks(); self.benchmark=ModelBenchmark()
        self.registry.register(ModelDescriptor("webster-local","deterministic",format="builtin",context_length=2048))
    def register_local(self,path):
        if not self.permissions.allowed("local",ModelPermissions.LOAD): raise PermissionError("model loading denied")
        descriptor,backend=self.loader.load(path); self.registry.register(descriptor)
        if backend is not None:self.engine.attach(descriptor,backend)
        return descriptor
    def generate(self,prompt,model_id=None,profile="eco",history=(),evidence=()):
        if not self.permissions.allowed("local",ModelPermissions.INFER): raise PermissionError("model inference denied")
        model=self.router.choose(self.registry.list(),model_id); key=(model.model_id,profile,prompt,tuple(history)[-4:],tuple(evidence)[-4:]); cached=self.cache.get(key)
        if cached:return cached
        self.guard.validate(128 if profile=="eco" else 256)
        response=self.guard.timed(self.generator.generate,prompt,model,history,evidence,profile)
        self.cache.put(key,response); self.learning.observe(response,type("Req",(),{"prompt":prompt})()); return response
    def respond(self,prompt,**kwargs):
        try:return self.generate(prompt,**kwargs)
        except Exception:
            return type("Response",(),{"text":self.offline.respond(prompt),"model_id":"offline","provider":"offline","confidence":0.45,"tokens":0,"latency_ms":0.0,"metadata":(("fallback","true"),)})()
    def status(self): return {"models":[m.model_id for m in self.registry.list()],"cache_items":len(self.cache._data),"learning":self.learning.summary()}
