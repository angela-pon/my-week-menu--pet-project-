from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(Text, default="")
    image_url = Column(String, nullable=True)

    ingredients = relationship(
        "Ingredient",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    category = Column(String, nullable=False)

    recipe = relationship("Recipe", back_populates="ingredients")
