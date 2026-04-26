import { useState, useEffect } from "react";
import { getShoppingList } from "../services/api";

function ShoppingListPage() {
  const [shoppingList, setShoppingList] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadShoppingList() {
      try {
        const weekStart = new Date().toISOString().split("T")[0];
        const data = await getShoppingList(weekStart);
        setShoppingList(data);
      } catch (error) {
        console.error("Failed to load shopping list:", error);
        setError("Failed to load shopping list");
      } finally {
        setLoading(false);
      }
    }
    loadShoppingList();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-gray-400">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-red-500">{error}</div>
      </div>
    );
  }

  const categoryKeys = ["vegetables", "meat", "dairy", "others"];
  const categories = categoryKeys.filter(
    (cat) => shoppingList[cat]?.length > 0,
  );

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">Shopping List</h1>
        <p className="text-gray-500 mt-1">Ingredients for this week's meals</p>
      </div>

      {categories.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No items in your shopping list yet.</p>
          <p className="text-gray-400 text-sm mt-2">
            Add meals to your meal plan first.
          </p>
        </div>
      ) : (
        <div className="space-y-8">
          {categories.map((category) => (
            <div
              key={category}
              className="bg-white rounded-xl border border-gray-100 p-6"
            >
              <h2 className="text-lg font-semibold text-gray-900 capitalize mb-4">
                {category}
              </h2>
              <ul className="space-y-2">
                {shoppingList[category].map((item, index) => (
                  <li key={index} className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      className="w-4 h-4 rounded border-gray-300 text-emerald-500 focus:ring-emerald-500"
                    />
                    <span className="text-gray-700">
                      {item.amount} {item.unit} {item.name}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ShoppingListPage;
