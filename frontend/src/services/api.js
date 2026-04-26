const BASE_URL = "http://127.0.0.1:8000";

export async function getRecipes() {
  const response = await fetch(`${BASE_URL}/api/recipes/`);
  if (!response.ok) throw new Error("Failed to fetch recipes");
  return response.json();
}

export async function createRecipe(recipe) {
  const response = await fetch(`${BASE_URL}/api/recipes/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(recipe),
  });
  if (!response.ok) throw new Error("Failed to create recipe");
  return response.json();
}

export async function getMealPlan(weekStart) {
  const response = await fetch(
    `${BASE_URL}/api/meal-plans/?week_start=${weekStart}`,
  );
  if (!response.ok) throw new Error("Failed to fetch meal plan");
  return response.json();
}

export async function saveMealPlan(weekStart, meals) {
  const response = await fetch(`${BASE_URL}/api/meal-plans/`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ week_start: weekStart, meals }),
  });
  if (!response.ok) throw new Error("Failed to save meal plan");
  return response.json();
}

export async function getShoppingList(weekStart) {
  const response = await fetch(
    `${BASE_URL}/api/shopping-list/?week_start=${weekStart}`,
  );
  if (!response.ok) throw new Error("Failed to fetch shopping list");
  return response.json();
}
