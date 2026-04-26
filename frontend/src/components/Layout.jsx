import { NavLink } from "react-router-dom";

const navItems = [
  { to: "/recipes", label: "Recipes" },
  { to: "/meal-plan", label: "Meal Plan" },
  { to: "/shopping-list", label: "Shopping List" },
];

function Layout({ children }) {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-100 sticky top-0 z-50">
        <nav className="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
          <NavLink
            to="/"
            className="text-xl font-semibold text-gray-900 hover:text-gray-600 transition-colors"
          >
            My Week Menu
          </NavLink>

          <div className="flex items-center gap-8">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `text-sm font-medium transition-colors ${
                    isActive
                      ? "text-gray-900"
                      : "text-gray-500 hover:text-gray-900"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </div>
        </nav>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-10">{children}</main>
    </div>
  );
}

export default Layout;
