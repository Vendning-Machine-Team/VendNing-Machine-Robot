import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import { resolve } from 'path'
import { fileURLToPath } from 'url'
import { dirname } from 'path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

export default defineConfig({
  base: './',
  plugins: [
    tailwindcss(),
  ],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
      },
    },
  },
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        adminDashboard: resolve(__dirname, 'pages/adminDashboard.html'),
        adminLogin: resolve(__dirname, 'pages/adminLogin.html'),
        paymentCode: resolve(__dirname, 'pages/paymentCode.html'),
        reportIssue: resolve(__dirname, 'pages/reportIssue.html'),
        setInventory: resolve(__dirname, 'pages/setInventory.html'),
        setPath: resolve(__dirname, 'pages/setPath.html'),
        viewActions: resolve(__dirname, 'pages/viewActions.html'),
      }
    }
  }
})