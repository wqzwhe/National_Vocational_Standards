import vue from '@vitejs/plugin-vue'

export default {
  plugins: [vue()],
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5050',
        changeOrigin: true
      }
    }
  }
}