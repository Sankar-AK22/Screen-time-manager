/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#007BFF',
          dark: '#0056b3',
        },
        accent: {
          DEFAULT: '#FF8800',
          dark: '#cc6d00',
        },
        dark: {
          bg: '#0B0B0B',
          card: '#1E1E1E',
          border: '#2A2A2A',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

