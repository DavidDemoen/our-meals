from datetime import datetime
from unittest.mock import Base

from sqlalchemy import DateTime, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.modules.recipe_group.recipe_management.models.recipe_table import RecipeTable


class TagTable(Base):
    __tablename__ = "tags"
    __table_args__ = (
        UniqueConstraint("name", name="uq_tag_name"),
        { "schema": "recipe_management" },
        )

    key: Mapped[int] = mapped_column(String(50), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=utc_now, onupdate=utc_now, nullable=False)
    deleted_at_utc: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    recipes: Mapped[list[RecipeTable]] = relationship(
        secondary=recipe_tags,
        back_populates="tags",
    )