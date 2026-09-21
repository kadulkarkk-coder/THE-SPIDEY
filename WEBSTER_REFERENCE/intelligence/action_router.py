"""Functional action routing from A5 interpretations to safe executable capabilities."""
from __future__ import annotations
from dataclasses import dataclass
import re
from typing import Any, Callable
from .intent_pipeline import IntelligenceInterpretation
from ..tools.tool_contract import ToolCall
from ..tools.tool_dispatcher import ToolDispatcher
from ..tools.tool_result import ToolResult
from ..tools.tool_confirmation import ToolConfirmationGate
from ..tools.tool_permissions import ToolPermissionPolicy

@dataclass(frozen=True)
class ActionResult:
    handled: bool
    ok: bool
    message: str
    target: str
    kind: str = "none"
    data: dict[str, Any] | None = None

    @classmethod
    def not_handled(cls) -> "ActionResult":
        return cls(False, True, "", "conversation")

class ActionRouter:
    """Turns an interpretation into an executable command/tool only when safe."""
    _TOOL_PATTERNS = (
        (re.compile(r"^\s*(?:calculate|calc)\s+(.+)$", re.I), "calculator"),
        (re.compile(r"^\s*(?:(?:what time is it)|(?:what is the (?:current )?time)|(?:current time))\??\s*$", re.I), "time"),
    )

    def __init__(self, command_handler: Callable[[str], str] | None = None, tool_dispatcher: ToolDispatcher | None = None, permissions: ToolPermissionPolicy | None = None, confirmation: ToolConfirmationGate | None = None) -> None:
        self.command_handler = command_handler
        self.tools = tool_dispatcher
        self.permissions = permissions or ToolPermissionPolicy()
        self.confirmation = confirmation or ToolConfirmationGate()
        self.principal = "webster"
        self.permissions.allow(self.principal, "local.compute")
        self.permissions.allow(self.principal, "runtime.read")

    def route(self, interpretation: IntelligenceInterpretation, *, request_id: str = "", confirmed: bool = False) -> ActionResult:
        if not interpretation.constraints_allowed:
            return ActionResult(True, False, "The requested action is blocked by its constraints.", interpretation.target)
        text = interpretation.text.strip()
        for pattern, tool_name in self._TOOL_PATTERNS:
            match = pattern.match(text)
            if match:
                if self.tools is None:
                    return ActionResult(True, False, "That tool is not available.", tool_name, "tool")
                arguments: dict[str, Any] = {}
                capability = "runtime.read"
                if tool_name == "calculator":
                    arguments["expression"] = match.group(1)
                    capability = "local.compute"
                binding = self.tools.registry.get(tool_name)
                if binding is None:
                    return ActionResult(True, False, "That tool is not registered.", tool_name, "tool")
                if not self.permissions.permitted(self.principal, capability):
                    return ActionResult(True, False, "Permission is required for that action.", tool_name, "tool")
                if not self.confirmation.check(binding, confirmed=confirmed):
                    return ActionResult(True, False, f"Confirmation is required to run {tool_name}.", tool_name, "tool")
                result: ToolResult = self.tools.dispatch(ToolCall(tool_name, arguments, request_id=request_id))
                if not result.ok:
                    return ActionResult(True, False, result.error or "Tool execution failed.", tool_name, "tool")
                return ActionResult(True, True, str(result.value), tool_name, "tool", {"tool": tool_name})
        command_target = interpretation.target
        if command_target in {"command_help", "runtime_status"} and self.command_handler:
            command_name = "help" if command_target == "command_help" else "status"
            return ActionResult(True, True, self.command_handler(command_name), command_name, "command")
        return ActionResult.not_handled()
