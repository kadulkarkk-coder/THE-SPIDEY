"""Deterministic command dispatcher for the WEBSTER runtime."""
from __future__ import annotations

from collections.abc import Callable
from threading import RLock
from typing import Any

from .command_contracts import CommandRequest, CommandResponse
from .errors import EmptyCommandError, UnknownCommandError

CommandHandler = Callable[[CommandRequest], str | CommandResponse]


class CommandDispatcher:
    """Maps command names to handlers without coupling handlers to the UI."""

    def __init__(self) -> None:
        self._handlers: dict[str, CommandHandler] = {}
        self._lock = RLock()

    def register(self, name: str, handler: CommandHandler) -> None:
        key = name.strip().lower()
        if not key:
            raise ValueError("Command name cannot be empty")
        with self._lock:
            if key in self._handlers:
                raise ValueError(f"Command already registered: {key}")
            self._handlers[key] = handler

    def handler_for(self, name: str) -> CommandHandler:
        key = name.strip().lower()
        with self._lock:
            handler = self._handlers.get(key)
        if handler is None:
            raise UnknownCommandError(f"Unknown command: {key}")
        return handler

    def dispatch(self, request: CommandRequest) -> CommandResponse:
        normalized = request.normalized()
        if not normalized.text:
            raise EmptyCommandError("Command cannot be empty")
        name = normalized.text.split(maxsplit=1)[0].lower()
        result = self.handler_for(name)(normalized)
        if isinstance(result, CommandResponse):
            return result
        return CommandResponse.success(normalized, str(result))

    def names(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(sorted(self._handlers))

    def count(self) -> int:
        return len(self.names())
