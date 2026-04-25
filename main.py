from fastapi import FastAPI

from database import Base, engine
from routers import meal_plans, recipes, shopping_list

app = FastAPI(title="Meal Planner")

Base.metadata.create_all(bind=engine)

app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
app.include_router(meal_plans.router, prefix="/meal-plans", tags=["meal plans"])
app.include_router(shopping_list.router, tags=["shopping list"])
