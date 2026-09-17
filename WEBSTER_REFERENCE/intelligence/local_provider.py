"""Local-first AI provider with deterministic reasoning fallbacks."""
from __future__ import annotations

import re

from .decision_engine import ProviderResponse
from .local_calculator import calculate
from .local_knowledge import LocalKnowledge


class LocalProvider:
    """Dependency-free provider that never requires an external AI service."""

    name = "local"

    def __init__(self) -> None:
        self.knowledge = LocalKnowledge()

    @staticmethod
    def _current_request(prompt: str) -> str:
        match = re.search(r"Current request:\s*(.*?)(?:\nRecent conversation:|$)", prompt, flags=re.I | re.S)
        return " ".join((match.group(1) if match else prompt).split())

    def generate(self, prompt: str) -> ProviderResponse:
        cleaned = self._current_request(prompt)
        if not cleaned:
            return ProviderResponse("Tell me what you need.", self.name, 1.0, (("mode", "local"),))

        if re.search(r"\b(what did i say|what was my last message|repeat my last message)\b", cleaned, re.I):
            turns = re.findall(r"\nuser:\s*(.+?)(?=\n|$)", prompt, flags=re.I)
            if turns:
                return ProviderResponse(f"Your latest message was: {turns[-1]}", self.name, 0.93, (("mode", "local"), ("source", "conversation")))

        known = self.knowledge.answer(cleaned)
        if known:
            return ProviderResponse(known, self.name, 0.96, (("mode", "local"), ("source", "builtin")))

        expression = re.sub(r"^(what is|calculate|compute|solve)\s+", "", cleaned, flags=re.I).rstrip("?")
        if re.fullmatch(r"[\d\s+\-*/%().×÷]+", expression):
            value = calculate(expression)
            if value is not None:
                return ProviderResponse(f"The answer is {value}.", self.name, 0.99, (("mode", "local"), ("source", "calculator")))

        if cleaned.endswith("?"):
            return ProviderResponse(
                "I can answer this locally when it matches my built-in knowledge or tools. For broader knowledge, an optional provider plugin can be enabled; WEBSTER does not require one to run.",
                self.name, 0.62, (("mode", "local"), ("source", "fallback")),
            )
        return ProviderResponse(
            f"I understood: {cleaned}. I can route this through WEBSTER's local tools and reasoning modules.",
            self.name, 0.70, (("mode", "local"), ("source", "intent")),
        )
