"""Small offline knowledge base used before any optional external provider."""
from __future__ import annotations

from datetime import datetime


class LocalKnowledge:
    """Answer common identity, capability and conversational questions locally."""

    def answer(self, prompt: str) -> str | None:
        text = " ".join(prompt.lower().split())
        if not text:
            return "Tell me what you need."
        if any(greet in text for greet in ("hello", "hi webster", "hey webster", "good morning", "good evening")):
            return "Hello. WEBSTER is online and ready."
        if "who are you" in text or "what are you" in text:
            return "I am WEBSTER, a local-first desktop intelligence platform."
        if "what can you do" in text or "your capabilities" in text:
            return "I can route commands, reason through local tasks, manage memory, use tools, and connect optional voice, vision, automation, browser, and remote-control modules."
        if "what time" in text or text == "time":
            return datetime.now().astimezone().strftime("The local time is %I:%M %p.")
        if "what date" in text or text == "date" or "today's date" in text:
            return datetime.now().astimezone().strftime("Today is %A, %d %B %Y.")
        if "are you online" in text or "are you running" in text:
            return "Yes. The local WEBSTER runtime is active."
        return None
