from datetime import datetime
import uuid

from sqlalchemy import UUID, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.operational_db.base import Base
from src.modules.recipe_group.recipe_management.models.recipe_ingredients_table import RecipeIngredientTable


class IngredientTable(Base):
    __tablename__ = "ingredients"
    __table_args__ = (
        UniqueConstraint("name", name="uq_ingredient_name"),
        { "schema": "recipe_management" },
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_key: Mapped[str | None] = mapped_column(String(100), ForeignKey("recipe_management.ingr_categories.key", ondelete="no"), nullable=True, index=True)
    default_unit: Mapped[str | None] = mapped_column(String(50), nullable=True)

    created_at_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=utc_now, onupdate=utc_now, nullable=False)
    deleted_at_utc: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    recipe_links: Mapped[list[RecipeIngredientTable]] = relationship(
        back_populates="ingredient",
        cascade="all, delete-orphan",
    )