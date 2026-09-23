"""Slim executable runtime exposing only Restart A, B and C capabilities."""
from __future__ import annotations
from .runtime.runtime_manager import RuntimeManager
from .desktop.desktop_controller import DesktopController
from .ai.local_ai_controller import LocalAIController
from .intelligence.local_calculator import calculate
from .memory.memory_store import MemoryStore

class ABCApplication:
    VERSION="WEBSTER A+B+C"
    def __init__(self):
        self.runtime=RuntimeManager(); self.desktop=DesktopController(); self.ai=LocalAIController(); self.memory=MemoryStore(); self.running=False
    def start(self):
        self.runtime.start(); self.running=True
    def stop(self):
        self.running=False; self.runtime.stop()
    def command(self,text):
        value=" ".join(text.strip().split()); low=value.casefold()
        if not value:return ""
        if low in {"exit","quit"}: self.stop(); return "WEBSTER stopped."
        if low=="status": return str({"version":self.VERSION,"running":self.running,"runtime":self.runtime.snapshot(),"ai":self.ai.status(),"memory":self.memory.count()})
        if low=="capabilities": return "A: local intelligence, calculation, runtime, bounded memory. B: Windows desktop, apps, windows, keyboard, mouse, clipboard, files, browser, screenshots, safe shell. C: local model registry, optional GGUF inference, tokenizer, routing, caching, resource guard, offline fallback and learning hooks."
        if low.startswith("remember "):
            rec=self.memory.put("note",value[9:].strip(),kind="user-note"); return "Remembered locally: "+str(rec.value)
        if low=="memory": return str([r.value for r in self.memory.all()])
        if low.startswith(("calc ","calculate ","compute ")):
            expr=value.split(" ",1)[1]; result=calculate(expr); return "The answer is "+str(result) if result is not None else "I could not safely calculate that."
        if low.startswith("ai "):
            r=self.ai.respond(value[3:].strip()); return r.text
        action=self.desktop.execute(value,approved=True)
        if action.handled:return action.message
        if low in {"hi","hello","hey webster"}: return "Hello! WEBSTER is online locally."
        if low in {"who are you","what are you"}: return "WEBSTER is a local-first AI operating platform."
        if low=="date":
            from datetime import datetime
            return datetime.now().astimezone().strftime("%A, %d %B %Y %H:%M:%S %Z")
        return self.ai.respond(value).text
