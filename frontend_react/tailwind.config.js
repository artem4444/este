/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./frontend_react/src/**/*.{js,jsx,ts,tsx}",
    //This ensures that Tailwind will only keep the styles that are being used in the src folder.

  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

