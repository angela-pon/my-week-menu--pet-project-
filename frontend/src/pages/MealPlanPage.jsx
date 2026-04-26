import { useState, useEffect } from "react";
import { getRecipes, getMealPlan, saveMealPlan } from "../services/api";

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function MealCard({ type, meal, onClick }) {
  return (
    <button
      onClick={onClick}
      className="w-full p-3 bg-gray-50 rounded-lg text-left hover:bg-gray-100 transition-colors"
    >
      <div className="text-xs font-medium text-gray-400 uppercase mb-1">
        {type}
      </div>
      <div className="text-sm text-gray-700">
        {meal?.recipe_name || (
          <span className="text-gray-400 italic">Select recipe</span>
        )}
      </div>
    </button>
  );
}

function DayCard({ day, meals, onSelectMeal }) {
  return (
    <div className="bg-white rounded-xl border border-gray-100 p-4">
      <div className="font-semibold text-gray-900 mb-3">{day}</div>
      <div className="space-y-2">
        <MealCard
          type="Lunch"
          meal={meals?.find((m) => m.meal_type === "lunch")}
          onClick={() => onSelectMeal(day, "lunch")}
        />
        <MealCard
          type="Dinner"
          meal={meals?.find((m) => m.meal_type === "dinner")}
          onClick={() => onSelectMeal(day, "dinner")}
        />
      </div>
    </div>
  );
}

function RecipeSelector({ recipes, onSelect, onClose }) {
  return (
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-xl w-full max-w-md mx-4 max-h-[80vh] overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-4 border-b border-gray-100">
          <h3 className="font-semibold text-gray-900">Select Recipe</h3>
        </div>
        <div className="p-4 overflow-y-auto max-h-[60vh]">
          {recipes.length === 0 ? (
            <p className="text-gray-500 text-center py-4">
              No recipes available
            </p>
          ) : (
            <div className="space-y-2">
              {recipes.map((recipe) => (
                <button
                  key={recipe.id}
                  onClick={() => onSelect(recipe)}
                  className="w-full p-3 text-left bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className="font-medium text-gray-900">{recipe.name}</div>
                  <div className="text-sm text-gray-500 truncate">
                    {recipe.description}
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
        <div className="p-4 border-t border-gray-100">
          <button
            onClick={onClose}
            className="w-full py-2 text-gray-600 hover:text-gray-900"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

function MealPlanPage() {
  const [mealPlan, setMealPlan] = useState({});
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [saving, setSaving] = useState(false);

  const weekStart = new Date().toISOString().split("T")[0];

  useEffect(() => {
    async function loadData() {
      try {
        const [recipesData, mealPlanData] = await Promise.all([
          getRecipes(),
          getMealPlan(weekStart),
        ]);
        setRecipes(recipesData);
        setMealPlan(mealPlanData);
      } catch (error) {
        console.error("Failed to load data:", error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [weekStart]);

  const handleSelectMeal = (day, mealType) => {
    setSelectedSlot({ day, mealType });
  };

  const handleSelectRecipe = async (recipe) => {
    if (!selectedSlot) return;

    const { day, mealType } = selectedSlot;
    const newMealPlan = { ...mealPlan };

    if (!newMealPlan[day]) {
      newMealPlan[day] = [];
    }

    // Remove existing meal of same type
    newMealPlan[day] = newMealPlan[day].filter((m) => m.meal_type !== mealType);

    // Add new meal
    newMealPlan[day].push({
      recipe_id: recipe.id,
      recipe_name: recipe.name,
      meal_type: mealType,
    });

    setMealPlan(newMealPlan);
    setSelectedSlot(null);

    // Save to API
    setSaving(true);
    try {
      const meals = Object.entries(newMealPlan).flatMap(([day, dayMeals]) =>
        dayMeals.map((m) => ({ day: day.toLowerCase(), ...m })),
      );
      await saveMealPlan(weekStart, meals);
    } catch (error) {
      console.error("Failed to save meal plan:", error);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-gray-400">Loading...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Meal Plan</h1>
          <p className="text-gray-500 mt-1">This week's menu</p>
        </div>
        {saving && <span className="text-sm text-gray-400">Saving...</span>}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-7 gap-4">
        {DAYS.map((day) => (
          <DayCard
            key={day}
            day={day}
            meals={mealPlan[day]}
            onSelectMeal={handleSelectMeal}
          />
        ))}
      </div>

      {selectedSlot && (
        <RecipeSelector
          recipes={recipes}
          onSelect={handleSelectRecipe}
          onClose={() => setSelectedSlot(null)}
        />
      )}
    </div>
  );
}

export default MealPlanPage;
