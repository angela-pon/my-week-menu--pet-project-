from typing import Literal

from pydantic import BaseModel, ConfigDict


IngredientUnit = Literal["g", "kg", "ml", "l", "pcs"]


class IngredientBase(BaseModel):
    name: str
    quantity: str
    unit: IngredientUnit
    category: str

    model_config = ConfigDict(from_attributes=True)


class IngredientCreate(IngredientBase):
    pass


class IngredientRead(IngredientBase):
    id: int


class RecipeBase(BaseModel):
    title: str
    description: str | None = None
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RecipeCreate(RecipeBase):
    ingredients: list[IngredientCreate] = []


class RecipeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    ingredients: list[IngredientCreate] | None = None

    model_config = ConfigDict(from_attributes=True)


class RecipeRead(RecipeBase):
    id: int
    ingredients: list[IngredientRead] = []

    model_config = ConfigDict(from_attributes=True)


class RecipeLightRead(BaseModel):
    id: int
    title: str
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)
