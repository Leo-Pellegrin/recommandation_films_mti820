export default defineNuxtConfig({
  modules: [
    '@pinia/nuxt',
    '@sidebase/nuxt-auth',
    '@nuxt/ui',
  ],

  // routeRules: {
  //   '/': { middleware: 'auth' }, 
  //   '/profile/**': { middleware: 'auth' },    
  // },
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