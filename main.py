from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import meal_plans, recipes, shopping_list

app = FastAPI(title="Meal Planner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(recipes.router, prefix="/api/recipes", tags=["recipes"])
app.include_router(meal_plans.router, prefix="/api/meal-plans", tags=["meal plans"])
app.include_router(shopping_list.router, prefix="/api/shopping-list", tags=["shopping list"])
