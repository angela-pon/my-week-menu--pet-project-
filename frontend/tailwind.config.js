/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter Tight", "system-ui", "sans-serif"],
      },
      colors: {
        primary: "#374151",
        secondary: "#6b7280",
      },
    },
  },
  plugins: [],
};
