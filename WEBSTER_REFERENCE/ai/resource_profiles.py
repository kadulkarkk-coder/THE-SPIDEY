"""Resource profiles tuned for modest Windows laptops."""
from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class ResourceProfile:
    name:str; max_context:int; max_tokens:int; temperature:float; max_seconds:float
PROFILES={
 "eco":ResourceProfile("eco",1024,128,0.1,8.0),
 "balanced":ResourceProfile("balanced",2048,256,0.2,15.0),
 "quality":ResourceProfile("quality",4096,512,0.3,30.0),
}
