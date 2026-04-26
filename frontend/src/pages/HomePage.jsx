import { useState, useEffect } from "react";
import { getRecipes, getMealPlan } from "../services/api";

function HomePage() {
  const [recipes, setRecipes] = useState([]);
  const [mealPlan, setMealPlan] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [recipesData, mealPlanData] = await Promise.all([
          getRecipes(),
          getMealPlan(new Date().toISOString().split("T")[0]),
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
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-gray-500">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-semibold text-gray-900">My Week Menu</h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <section className="mb-8">
          <h2 className="text-lg font-medium text-gray-900 mb-4">This Week</h2>
          <div className="grid grid-cols-7 gap-2">
            {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((day) => (
              <div
                key={day}
                className="bg-white rounded-lg border border-gray-200 p-3 min-h-[100px]"
              >
                <div className="text-sm font-medium text-gray-500 mb-2">
                  {day}
                </div>
                <div className="text-sm text-gray-400">No meal</div>
              </div>
            ))}
          </div>
        </section>

        <section>
          <h2 className="text-lg font-medium text-gray-900 mb-4">Recipes</h2>
          <div className="bg-white rounded-lg border border-gray-200 p-6 text-center text-gray-500">
            No recipes yet. Add your first recipe!
          </div>
        </section>
      </main>
    </div>
  );
}

export default HomePage;
