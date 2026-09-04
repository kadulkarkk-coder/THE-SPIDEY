"""Privacy-aware visual context boundary for multimodal requests."""
from __future__ import annotations
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class VisualContext:
    description: str
    source: str = "unknown"
    redacted: bool = False


class VisualContextBuilder:
    _EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
    _PHONE = re.compile(r"(?<!\d)(?:\+?\d[\d ()-]{7,}\d)(?!\d)")

    def build(self, description: str, *, source: str = "unknown", redact: bool = True) -> VisualContext:
        text = " ".join(description.split())
        if redact:
            text = self._EMAIL.sub("[REDACTED_EMAIL]", text)
            text = self._PHONE.sub("[REDACTED_PHONE]", text)
        return VisualContext(text, source.strip() or "unknown", redact)
