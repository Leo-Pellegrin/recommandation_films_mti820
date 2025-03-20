export default defineNuxtConfig({
  modules: [
    '@pinia/nuxt',
    '@sidebase/nuxt-auth' // Si tu utilises l'authentification
  ],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api'
    }
  },

  typescript: {
    strict: true
  },

  compatibilityDate: '2025-03-20'
})