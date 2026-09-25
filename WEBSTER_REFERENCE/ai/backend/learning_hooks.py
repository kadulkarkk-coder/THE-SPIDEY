"""Observation hooks for future learning without self-modifying core code."""
from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class LearningRecord:
    prompt:str; model_id:str; ok:bool; latency_ms:float; confidence:float
class LearningHooks:
    def __init__(self,max_records=200): self.max_records=max_records; self.records=[]
    def observe(self,response,request):
        self.records.append(LearningRecord(request.prompt,response.model_id,bool(response.text),response.latency_ms,response.confidence))
        if len(self.records)>self.max_records:self.records=self.records[-self.max_records:]
    def summary(self): return {"samples":len(self.records),"successes":sum(r.ok for r in self.records)}
