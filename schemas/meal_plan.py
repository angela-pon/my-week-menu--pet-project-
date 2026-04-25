from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict


MealType = Literal["lunch", "dinner"]


class MealEntryBase(BaseModel):
    date: date
    meal_type: MealType
    recipe_id: int

    model_config = ConfigDict(from_attributes=True)


class MealEntryCreate(MealEntryBase):
    pass


class MealEntryRead(MealEntryBase):
    id: int
    meal_plan_id: int


class MealPlanBase(BaseModel):
    week_start_date: date

    model_config = ConfigDict(from_attributes=True)


class MealPlanCreate(MealPlanBase):
    pass


class MealPlanRead(MealPlanBase):
    id: int
    entries: list[MealEntryRead] = []

    model_config = ConfigDict(from_attributes=True)


class MealPlanCalendarSlot(BaseModel):
    date: date
    weekday: str
    lunch: str | None = None
    dinner: str | None = None


class MealPlanCalendarRead(BaseModel):
    meal_plan_id: int
    week_start_date: date
    schedule: list[MealPlanCalendarSlot] = []

    model_config = ConfigDict(from_attributes=True)


class ShoppingListItem(BaseModel):
    name: str
    quantity: float | int
    unit: str


class ShoppingListRead(BaseModel):
    meal_plan_id: int
    week_start_date: date
    vegetables: list[ShoppingListItem] = []
    meat: list[ShoppingListItem] = []
    dairy: list[ShoppingListItem] = []
    others: list[ShoppingListItem] = []

    model_config = ConfigDict(from_attributes=True)
