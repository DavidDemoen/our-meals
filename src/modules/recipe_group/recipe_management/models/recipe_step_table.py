import uuid

from sqlalchemy import UUID, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.operational_db.base import Base
from src.modules.recipe_group.recipe_management.models.recipe_table import RecipeTable


class RecipeStepTable(Base):
    __tablename__ = "recipe_steps"
    __table_args__ = (
        UniqueConstraint("recipe_id", "step_number", name="uq_recipe_step_number"),
        { "schema": "recipe_management" },
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    step_number: Mapped[int] = mapped_column(Integer, nullable=False)
    instruction: Mapped[str] = mapped_column(Text, nullable=False)

    recipe: Mapped[RecipeTable] = relationship(back_populates="steps")