"""Categorized errors for the tool execution boundary."""
from __future__ import annotations

class ToolError(Exception):
    code = "TOOL_ERROR"

class ToolNotFoundError(ToolError):
    code = "NOT_FOUND"

class ToolPermissionError(ToolError):
    code = "PERMISSION_DENIED"

class ToolValidationError(ToolError):
    code = "INVALID_ARGUMENTS"

class ToolConfirmationRequired(ToolError):
    code = "CONFIRMATION_REQUIRED"
