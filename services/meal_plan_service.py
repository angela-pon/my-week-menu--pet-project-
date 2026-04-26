from collections import defaultdict
from datetime import date
import re
from typing import Any

from sqlalchemy.orm import Session, joinedload

from models.meal import MealEntry, MealPlan
from models.recipe import Recipe
from schemas.meal_plan import MealEntryCreate, MealPlanCreate

CATEGORY_MAP = {
    "vegetables": "vegetables",
    "vegetable": "vegetables",
    "meat": "meat",
    "dairy": "dairy",
}

UNIT_BASE = {
    "g": ("g", 1),
    "kg": ("g", 1000),
    "ml": ("ml", 1),
    "l": ("ml", 1000),
    "pcs": ("pcs", 1),
}

NORMALIZE_THRESHOLD = {
    "g": (1000, "kg"),
    "ml": (1000, "l"),
}


def _parse_quantity(quantity_text: str) -> float:
    try:
        return float(quantity_text)
    except ValueError:
        match = re.search(r"[0-9]+(?:[.,][0-9]+)?", quantity_text)
        if not match:
            return 0.0
        normalized = match.group(0).replace(",", ".")
        return float(normalized)


def _normalize_category(category: str) -> str:
    return CATEGORY_MAP.get(category.strip().lower(), "others")


def _convert_to_base(quantity: float, unit: str) -> tuple[float, str]:
    unit_key = unit.strip().lower()
    base_unit, multiplier = UNIT_BASE.get(unit_key, (unit_key, 1))
    return quantity * multiplier, base_unit


def _format_quantity(value: float) -> float | int:
    if value.is_integer():
        return int(value)
    return round(value, 2)


def _normalize_output(quantity: float, base_unit: str) -> tuple[float | int, str]:
    if base_unit in NORMALIZE_THRESHOLD:
        threshold, normalized_unit = NORMALIZE_THRESHOLD[base_unit]
        if quantity >= threshold:
            return _format_quantity(quantity / threshold), normalized_unit
    return _format_quantity(quantity), base_unit


def create_meal_plan(session: Session, meal_plan_in: MealPlanCreate) -> MealPlan:
    plan = MealPlan(week_start_date=meal_plan_in.week_start_date)
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


def add_meal_entry(session: Session, meal_plan_id: int, entry_in: MealEntryCreate) -> MealPlan | None:
    plan = session.get(MealPlan, meal_plan_id)
    if not plan:
        return None

    entry = MealEntry(
        meal_plan_id=meal_plan_id,
        date=entry_in.date,
        meal_type=entry_in.meal_type,
        recipe_id=entry_in.recipe_id,
    )
    session.add(entry)
    session.commit()
    session.refresh(plan)
    return plan


def get_meal_plan(session: Session, meal_plan_id: int) -> MealPlan | None:
    return session.get(MealPlan, meal_plan_id)


def get_or_create_meal_plan(session: Session, week_start: str) -> MealPlan:
    """Get or create a meal plan for the given week start date."""
    from datetime import datetime
    week_start_date = datetime.strptime(week_start, "%Y-%m-%d").date()
    
    plan = session.query(MealPlan).filter(MealPlan.week_start_date == week_start_date).first()
    if not plan:
        plan = MealPlan(week_start_date=week_start_date)
        session.add(plan)
        session.commit()
        session.refresh(plan)
    return plan


def _get_meal_plan_with_entries(
    session: Session, meal_plan_id: int, load_ingredients: bool = False
) -> MealPlan | None:
    options = joinedload(MealPlan.entries).joinedload(MealEntry.recipe)
    if load_ingredients:
        options = options.joinedload(Recipe.ingredients)

    return (
        session.query(MealPlan)
        .options(options)
        .filter(MealPlan.id == meal_plan_id)
        .first()
    )


def get_meal_plan_calendar(session: Session, meal_plan_id: int) -> dict | None:
    plan = _get_meal_plan_with_entries(session, meal_plan_id)
    if not plan:
        return None

    rows: dict[date, dict[str, Any]] = {}
    for entry in plan.entries:
        row = rows.setdefault(
            entry.date,
            {
                "date": entry.date,
                "weekday": entry.date.strftime("%A"),
                "lunch": None,
                "dinner": None,
            },
        )
        if entry.meal_type == "lunch":
            row["lunch"] = entry.recipe.title
        elif entry.meal_type == "dinner":
            row["dinner"] = entry.recipe.title

    schedule = [rows[key] for key in sorted(rows)]
    return {
        "meal_plan_id": meal_plan_id,
        "week_start_date": plan.week_start_date.isoformat(),
        "schedule": schedule,
    }


def get_meal_plans(session: Session) -> list[MealPlan]:
    return session.query(MealPlan).all()


def build_shopping_list(session: Session, meal_plan_id: int) -> dict | None:
    plan = _get_meal_plan_with_entries(session, meal_plan_id, load_ingredients=True)
    if not plan:
        return None

    aggregated: dict[tuple[str, str, str], dict[str, Any]] = {}

    for entry in plan.entries:
        recipe = entry.recipe
        for ingredient in recipe.ingredients:
            category = _normalize_category(ingredient.category)
            quantity = _parse_quantity(ingredient.quantity)
            base_quantity, base_unit = _convert_to_base(quantity, ingredient.unit)
            key = (category, ingredient.name.strip().lower(), base_unit)

            if key not in aggregated:
                aggregated[key] = {
                    "name": ingredient.name.strip(),
                    "quantity": 0.0,
                    "unit": base_unit,
                    "category": category,
                }
            aggregated[key]["quantity"] += base_quantity

    grouped = {"vegetables": [], "meat": [], "dairy": [], "others": []}
    for item in aggregated.values():
        quantity, unit = _normalize_output(item["quantity"], item["unit"])
        grouped[item["category"]].append(
            {
                "name": item["name"],
                "quantity": quantity,
                "unit": unit,
            }
        )

    return {
        "meal_plan_id": meal_plan_id,
        "week_start_date": plan.week_start_date,
        "vegetables": grouped["vegetables"],
        "meat": grouped["meat"],
        "dairy": grouped["dairy"],
        "others": grouped["others"],
    }
