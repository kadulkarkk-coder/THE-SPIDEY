"""Safe loader for optional local model manifests and optional llama.cpp backends."""
from __future__ import annotations
import json
from pathlib import Path
from .model_contracts import ModelDescriptor

class ModelLoader:
    ALLOWED={"gguf","json","builtin","text"}
    def inspect(self,path:str)->ModelDescriptor:
        p=Path(path).expanduser().resolve()
        if not p.is_file(): raise FileNotFoundError(p)
        ext=p.suffix.lower().lstrip(".") or "text"
        if ext not in self.ALLOWED: raise ValueError(f"unsupported local model format: {ext}")
        meta={}
        if ext=="json":
            try:
                raw=json.loads(p.read_text(encoding="utf-8")); meta={str(k):str(v) for k,v in raw.items() if isinstance(v,(str,int,float,bool))}
            except Exception: meta={}
        return ModelDescriptor(p.stem,path=str(p),format=ext,metadata=tuple(sorted(meta.items())))
    def load(self,path:str):
        d=self.inspect(path)
        if d.format=="gguf":
            try:
                from llama_cpp import Llama
            except ImportError as exc: raise RuntimeError("GGUF support requires optional llama-cpp-python") from exc
            return d,Llama(model_path=d.path,n_ctx=d.context_length,verbose=False)
        return d,None
