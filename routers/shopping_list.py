from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_session
from schemas.meal_plan import ShoppingListRead
from services.meal_plan_service import build_shopping_list

router = APIRouter()


@router.get("/shopping-list/{meal_plan_id}", response_model=ShoppingListRead)
def get_shopping_list(meal_plan_id: int, session: Session = Depends(get_session)) -> ShoppingListRead:
    shopping = build_shopping_list(session, meal_plan_id)
    if shopping is None:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    return shopping
