from typing import Type

from src.application.contracts.messaging.messaging import AppCommand, AppEvent, AppMessage, Handler
from src.infrastructure.message_bus.abstr_message_bus import AbstractMessageBus
from src.infrastructure.message_bus.handler_registry import HandlerRegistry


class InMemoryMessageBus(AbstractMessageBus):
    """Simple in-memory message bus for development and testing.

    Uses a HandlerRegistry that distinguishes:
    - Commands: one handler per command type (raises if duplicate)
    - Events: multiple handlers per event type

    Handlers are called synchronously when `handle` is invoked.
    """

    def __init__(self, registry: HandlerRegistry | None = None) -> None:
        self._registry = registry or HandlerRegistry()

    def register(self, message_type: Type[AppMessage], handler: Handler) -> None:
        """Register a handler for a message type (command or event)."""
        if issubclass(message_type, AppCommand):
            self._registry.register_command(message_type, handler)
        elif issubclass(message_type, AppEvent):
            self._registry.register_event(message_type, handler)
        else:
            raise ValueError(f"Unknown message type: {message_type}")

    def handle(self, message: AppMessage) -> None:
        """Dispatch a message to its registered handler(s).

        Commands are dispatched to their single handler.
        Events are dispatched to all registered handlers.
        """
        message_type = type(message)

        if isinstance(message, AppCommand):
            handler = self._registry.get_command_handler(
                message_type  # type: ignore
            )
            if handler:
                handler(message)
        elif isinstance(message, AppEvent):
            handlers = self._registry.get_event_handlers(
                message_type  # type: ignore
            )
            for handler in handlers:
                handler(message)
