"""Local generator combining context, tokenizer and inference."""
from __future__ import annotations
from .model_contracts import GenerationRequest,GenerationResponse,ModelDescriptor
from .inference_engine import InferenceEngine
from .prompt_context import PromptContext
from .resource_profiles import PROFILES
class LocalGenerator:
    def __init__(self,engine=None): self.engine=engine or InferenceEngine(); self.context=PromptContext()
    def generate(self,prompt,model,history=(),evidence=(),profile="eco"):
        cfg=PROFILES.get(profile,PROFILES["eco"]); built=self.context.build("You are WEBSTER, concise and factual.",prompt,history,evidence)
        req=GenerationRequest(built,max_tokens=cfg.max_tokens,temperature=cfg.temperature,model_id=model.model_id)
        return self.engine.generate(req,model)
