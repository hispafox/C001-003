import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Proxy para evitar problemas de CORS durante desarrollo.
    // Todas las peticiones a /api se reenvían al backend .NET.
    proxy: {
      '/api': {
        target: 'https://localhost:7272',
        changeOrigin: true,
        secure: false, // acepta certificado auto-firmado de desarrollo
      },
    },
  },
})
