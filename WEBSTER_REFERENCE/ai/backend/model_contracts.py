"""Stable contracts for local model execution."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ModelDescriptor:
    model_id: str
    family: str="deterministic"
    path: str|None=None
    format: str="builtin"
    context_length: int=2048
    quantization: str="none"
    metadata: tuple[tuple[str,str],...]=()

@dataclass(frozen=True)
class GenerationRequest:
    prompt: str
    max_tokens: int=256
    temperature: float=0.2
    model_id: str|None=None
    system: str="You are WEBSTER, a local-first assistant."
    metadata: dict[str,Any]=field(default_factory=dict)

@dataclass(frozen=True)
class GenerationResponse:
    text: str
    model_id: str
    provider: str="local"
    tokens: int=0
    latency_ms: float=0.0
    confidence: float=0.5
    metadata: tuple[tuple[str,str],...]=()
