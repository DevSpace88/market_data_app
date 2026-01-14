import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_API_BASE_URL || 'http://localhost:8000',
        changeOrigin: true,
        ws: true
      },
      '/ws': {
        target: process.env.VITE_API_BASE_URL?.replace('http', 'ws') || 'ws://localhost:8000',
        ws: true,
        changeOrigin: true
      }
    }
  },
  preview: {
    host: '0.0.0.0',
    port: parseInt(process.env.PORT || '3000')
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'terser'
  }
})
