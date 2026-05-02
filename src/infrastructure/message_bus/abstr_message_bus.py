from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type

from src.application.contracts.messaging.messaging import AppMessage, Handler


class AbstractMessageBus(ABC):
    """Abstract message bus defining the minimal interface for message handling.

    Concrete implementations must implement `register` to attach handlers
    and `handle` to dispatch published messages to registered handlers.
    """

    @abstractmethod
    def register(self, message_type: Type[AppMessage], handler: Handler) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle(self, message: AppMessage) -> None:
        raise NotImplementedError
