const { setupInspiraUI } = require('@inspira-ui/plugins')

module.exports = {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {}
  },
  plugins: [setupInspiraUI, require('tailwindcss-animate')]
}