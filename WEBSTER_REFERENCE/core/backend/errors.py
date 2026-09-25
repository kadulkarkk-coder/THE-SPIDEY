"""Controlled exception hierarchy for the WEBSTER runtime."""
from __future__ import annotations


class WebsterError(Exception):
    """Base class for expected WEBSTER runtime failures."""


class CommandError(WebsterError):
    """Base class for command-processing failures."""


class EmptyCommandError(CommandError):
    """Raised when a request contains no executable command."""


class UnknownCommandError(CommandError):
    """Raised when no registered handler matches a command."""


class RuntimeStateError(WebsterError):
    """Raised when an operation is invalid for the current runtime state."""
