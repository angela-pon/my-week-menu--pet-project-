from sqlalchemy.orm import Session, load_only

from models.recipe import Ingredient, Recipe
from schemas.recipe import IngredientCreate, RecipeCreate, RecipeUpdate


def _build_ingredients(ingredients: list[IngredientCreate]) -> list[Ingredient]:
    return [
        Ingredient(
            name=ingredient.name,
            quantity=ingredient.quantity,
            unit=ingredient.unit,
            category=ingredient.category,
        )
        for ingredient in ingredients
    ]


def create_recipe(session: Session, recipe_in: RecipeCreate) -> Recipe:
    recipe = Recipe(
        title=recipe_in.title,
        description=recipe_in.description or "",
        image_url=recipe_in.image_url,
    )
    recipe.ingredients = _build_ingredients(recipe_in.ingredients)

    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe


def get_recipes(session: Session) -> list[Recipe]:
    return session.query(Recipe).all()


def get_recipes_light(session: Session) -> list[Recipe]:
    return session.query(Recipe).options(load_only(Recipe.id, Recipe.title, Recipe.image_url)).all()


def get_recipe(session: Session, recipe_id: int) -> Recipe | None:
    return session.get(Recipe, recipe_id)


def update_recipe(session: Session, recipe_id: int, recipe_in: RecipeUpdate) -> Recipe | None:
    recipe = get_recipe(session, recipe_id)
    if not recipe:
        return None

    if recipe_in.title is not None:
        recipe.title = recipe_in.title
    if recipe_in.description is not None:
        recipe.description = recipe_in.description
    if recipe_in.image_url is not None:
        recipe.image_url = recipe_in.image_url
    if recipe_in.ingredients is not None:
        recipe.ingredients = _build_ingredients(recipe_in.ingredients)

    session.commit()
    session.refresh(recipe)
    return recipe


def delete_recipe(session: Session, recipe_id: int) -> bool:
    recipe = get_recipe(session, recipe_id)
    if not recipe:
        return False

    session.delete(recipe)
    session.commit()
    return True
