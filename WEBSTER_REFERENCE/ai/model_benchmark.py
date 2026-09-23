"""Small on-device benchmark harness; no long-running benchmark loop."""
from __future__ import annotations
import time
class ModelBenchmark:
    def run(self,generator,model,prompts=("hello","what can you do?")):
        rows=[]
        for p in prompts[:4]:
            t=time.perf_counter(); r=generator.generate(p,model); ms=(time.perf_counter()-t)*1000
            rows.append({"prompt":p,"latency_ms":round(ms,2),"tokens":r.tokens,"ok":bool(r.text)})
        return {"model_id":model.model_id,"samples":rows,"passed":all(x["ok"] for x in rows)}
