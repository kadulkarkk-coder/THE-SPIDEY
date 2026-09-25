"""Explicit confirmation boundary for tools that require user approval."""
from __future__ import annotations
from .tool_contract import ToolBinding

class ToolConfirmationGate:
    def check(self, binding: ToolBinding, *, confirmed: bool = False) -> bool:
        if not binding.spec.requires_confirmation:
            return True
        return confirmed
