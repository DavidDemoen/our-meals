from contextlib import contextmanager
from collections.abc import Callable, Iterator

from sqlalchemy.orm import Session, sessionmaker

from src.infrastructure.database.operational_db.db_engine import get_db_engine


SessionFactory = sessionmaker(
    bind=get_db_engine(),
    autoflush=False,
    autocommit=False,
)


class SessionManager:
    def __init__(self, factory: Callable[[], Session]):
        self._factory = factory

    def __call__(self) -> Session:
        return self._factory()

    @contextmanager
    def context(self) -> Iterator[Session]:
        """Context manager for safe usage."""
        db = self._factory()
        try:
            yield db
        finally:
            db.close()


session_manager = SessionManager(SessionFactory)