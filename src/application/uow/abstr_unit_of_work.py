from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import List, Optional, Type

from sqlalchemy.orm import Session

from src.application.contracts.messaging.messaging import AppMessage
from src.infrastructure.message_bus.abstr_message_bus import AbstractMessageBus


class AbstractUnitOfWork(ABC):
    """Abstract Unit of Work implementing the transaction script and publisher pattern.

    Manages the database session lifecycle, repository access, message collection,
    and atomic transaction handling with event publishing on successful commit.
    """

    def __init__(self, session: Session, message_bus: AbstractMessageBus) -> None:
        self._session: Session = session
        self._message_bus: AbstractMessageBus = message_bus
        self._messages: List[AppMessage] = []

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if exc_type:
            self.rollback()
        else:
            try:
                self.commit()
                self._publish_messages()
            except Exception:
                self.rollback()
                raise

    @abstractmethod
    def commit(self) -> None:
        """Commit the transaction.

        Subclasses must implement database-specific commit logic.
        Messages are published after a successful commit.
        """
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        """Rollback the transaction.

        Subclasses must implement database-specific rollback logic.
        Messages are discarded on rollback.
        """
        raise NotImplementedError

    def collect(self, message: AppMessage) -> None:
        """Queue a domain event for publishing after commit.

        Messages are dispatched to registered handlers in order
        after the transaction commits successfully.
        """
        self._messages.append(message)

    def _publish_messages(self) -> None:
        """Dispatch all collected messages to the message bus."""
        for message in self._messages:
            self._message_bus.handle(message)
        self._messages.clear()
