from typing import Callable
from uuid import UUID
import uuid

from pydantic import BaseModel


class AppMessage(BaseModel):
    id: UUID = uuid.uuid4()


class AppEvent(AppMessage):
    pass


class AppCommand(AppMessage):
    pass


Handler = Callable[[AppMessage], None]

