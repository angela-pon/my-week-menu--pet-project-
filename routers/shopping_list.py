from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_session
from schemas.meal_plan import ShoppingListRead
from services.meal_plan_service import build_shopping_list, get_or_create_meal_plan

router = APIRouter()


@router.get("/", response_model=ShoppingListRead)
def get_shopping_list(
    week_start: str = Query(...),
    session: Session = Depends(get_session)
) -> ShoppingListRead:
    """Get shopping list for a meal plan by week start date."""
    meal_plan = get_or_create_meal_plan(session, week_start)
    shopping = build_shopping_list(session, meal_plan.id)
    if shopping is None:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    return shopping
