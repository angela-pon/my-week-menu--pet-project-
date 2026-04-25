from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_session
from schemas.recipe import RecipeCreate, RecipeLightRead, RecipeRead, RecipeUpdate
from services.recipe_service import (
    create_recipe,
    delete_recipe,
    get_recipe,
    get_recipes,
    get_recipes_light,
    update_recipe,
)

router = APIRouter()


@router.post("/", response_model=RecipeRead)
def create(recipe_in: RecipeCreate, session: Session = Depends(get_session)) -> RecipeRead:
    return create_recipe(session, recipe_in)


@router.get("/", response_model=list[RecipeRead])
def list_recipes(session: Session = Depends(get_session)) -> list[RecipeRead]:
    return get_recipes(session)


@router.get("/light", response_model=list[RecipeLightRead])
def list_recipes_light(session: Session = Depends(get_session)) -> list[RecipeLightRead]:
    return get_recipes_light(session)


@router.get("/{recipe_id}", response_model=RecipeRead)
def read_recipe(recipe_id: int, session: Session = Depends(get_session)) -> RecipeRead:
    recipe = get_recipe(session, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.put("/{recipe_id}", response_model=RecipeRead)
def update(recipe_id: int, recipe_in: RecipeUpdate, session: Session = Depends(get_session)):
    recipe = update_recipe(session, recipe_id, recipe_in)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.delete("/{recipe_id}")
def delete(recipe_id: int, session: Session = Depends(get_session)):
    if not delete_recipe(session, recipe_id):
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"detail": "Recipe deleted"}
