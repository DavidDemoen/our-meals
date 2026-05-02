from __future__ import annotations

from typing import Dict, List, Type

from src.application.contracts.messaging.messaging import (
    AppCommand,
    AppEvent,
    Handler,
)


class HandlerRegistry:
    """Registry managing command and event handlers.

    Commands have exactly one handler (one-to-one).
    Events can have multiple handlers (one-to-many).
    """

    def __init__(self) -> None:
        self._command_handlers: Dict[Type[AppCommand], Handler] = {}
        self._event_handlers: Dict[Type[AppEvent], List[Handler]] = {}

    def register_command(self, command_type: Type[AppCommand], handler: Handler) -> None:
        """Register a single handler for a command.

        Raises ValueError if a handler is already registered for this command.
        """
        if command_type in self._command_handlers:
            raise ValueError(
                f"Handler already registered for command {command_type.__name__}"
            )
        self._command_handlers[command_type] = handler

    def register_event(self, event_type: Type[AppEvent], handler: Handler) -> None:
        """Register a handler for an event (multiple listeners allowed)."""
        self._event_handlers.setdefault(event_type, []).append(handler)

    def get_command_handler(self, command_type: Type[AppCommand]) -> Handler | None:
        """Retrieve the handler for a command, or None if not registered."""
        return self._command_handlers.get(command_type)

    def get_event_handlers(self, event_type: Type[AppEvent]) -> List[Handler]:
        """Retrieve all handlers for an event."""
        return self._event_handlers.get(event_type, [])
