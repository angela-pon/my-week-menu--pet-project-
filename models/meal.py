from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    week_start_date = Column(Date, nullable=False)

    entries = relationship(
        "MealEntry",
        back_populates="meal_plan",
        cascade="all, delete-orphan",
    )


class MealEntry(Base):
    __tablename__ = "meal_entries"

    id = Column(Integer, primary_key=True, index=True)
    meal_plan_id = Column(Integer, ForeignKey("meal_plans.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    date = Column(Date, nullable=False)
    meal_type = Column(String, nullable=False)

    meal_plan = relationship("MealPlan", back_populates="entries")
    recipe = relationship("Recipe")
