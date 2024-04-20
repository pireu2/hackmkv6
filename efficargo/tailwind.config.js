/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/templates/app/*.html', '../app/**/*.html'],
  theme: {
    extend: {},
  },
  plugins: [],
  purge: ['./app/templates/app/*.html', '../app/**/*.html']
}

