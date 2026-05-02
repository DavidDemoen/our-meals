from datetime import datetime
import uuid

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.operational_db.base import Base
from src.modules.recipe_group.recipe_management.models.recipe_step_table import RecipeStepTable


class RecipeTable(Base):
    __tablename__ = "recipes"
    __table_args__ = {"schema": "recipe_management"}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    author_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    servings: Mapped[int | None] = mapped_column(Integer, nullable=True)
    prep_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cook_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    difficulty: Mapped[int | None] = mapped_column(Integer, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    created_at_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=utc_now, onupdate=utc_now, nullable=False)
    deleted_at_utc: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    steps: Mapped[list[RecipeStepTable]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
        order_by="RecipeStepTable.step_number",
    )
    ingredients: Mapped[list[RecipeIngredientTable]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    tags: Mapped[list[TagTable]] = relationship(
        secondary=recipe_tags,
        back_populates="recipes",
    )
    