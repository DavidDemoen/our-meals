from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.operational_db.base import Base
from src.modules.recipe_group.recipe_management.models.ingredients_table import IngredientTable
from src.modules.recipe_group.recipe_management.models.recipe_table import RecipeTable


class RecipeIngredientTable(Base):
    __tablename__ = "recipe_ingredients"
    __table_args__ = {"schema": "recipe_management"}

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    quantity: Mapped[float | None] = mapped_column(nullable=True)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)

    created_at_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=utc_now, onupdate=utc_now, nullable=False)
    deleted_at_utc: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    recipe: Mapped[RecipeTable] = relationship(back_populates="ingredients")
    ingredient: Mapped[IngredientTable] = relationship(back_populates="recipe_links")