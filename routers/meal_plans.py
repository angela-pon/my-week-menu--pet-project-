from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_session
from schemas.meal_plan import (
    MealEntryCreate,
    MealPlanCalendarRead,
    MealPlanCreate,
    MealPlanRead,
)
from services.meal_plan_service import (
    add_meal_entry,
    build_shopping_list,
    create_meal_plan,
    get_meal_plan,
    get_meal_plan_calendar,
    get_meal_plans,
)

router = APIRouter()


@router.post("/", response_model=MealPlanRead)
def create(meal_plan_in: MealPlanCreate, session: Session = Depends(get_session)):
    return create_meal_plan(session, meal_plan_in)


@router.post("/{meal_plan_id}/entries", response_model=MealPlanRead)
def add_entry(meal_plan_id: int, entry_in: MealEntryCreate, session: Session = Depends(get_session)):
    meal_plan = add_meal_entry(session, meal_plan_id, entry_in)
    if not meal_plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    return meal_plan


@router.get("/{meal_plan_id}", response_model=MealPlanRead)
def get_plan(meal_plan_id: int, session: Session = Depends(get_session)) -> MealPlanRead:
    meal_plan = get_meal_plan(session, meal_plan_id)
    if not meal_plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    return meal_plan


@router.get("/{meal_plan_id}/calendar", response_model=MealPlanCalendarRead)
def get_plan_calendar(meal_plan_id: int, session: Session = Depends(get_session)) -> MealPlanCalendarRead:
    calendar = get_meal_plan_calendar(session, meal_plan_id)
    if not calendar:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    return calendar


@router.get("/", response_model=list[MealPlanRead])
def list_plans(session: Session = Depends(get_session)) -> list[MealPlanRead]:
    return get_meal_plans(session)
