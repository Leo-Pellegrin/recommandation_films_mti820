import tailwindcss from "@tailwindcss/vite";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: [
    '@pinia/nuxt',
    '@sidebase/nuxt-auth',
    '@nuxt/ui',
    'pinia-plugin-persistedstate/nuxt'
  ],
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
  auth: {
    isEnabled: true, // Active l'authentification
    originEnvKey: 'AUTH_ORIGIN', // Définit l'origine dans le fichier `.env`  
    disableServerSideAuth: false, // Permet l'auth côté serveur (décocher si tu veux uniquement côté client)

    sessionRefresh: {
      enablePeriodically: false,
      enableOnWindowFocus: false,
    },
    provider: {
      type: 'local',
      endpoints: {
        signUp: { path: '/register', method: 'post' },
        getSession: { path: '/me', method: 'get' }
      },
      pages: {
        login: '/auth/login',
      },
      token: {
        signInResponseTokenPointer: "/access_token", // Indique où récupérer le token dans la réponse API
        type: "Bearer",
        cookieName: "auth.token",
        headerName: "Authorization",
        maxAgeInSeconds: 1800,
        sameSiteAttribute: "lax",
        cookieDomain: "localhost",
        secureCookieAttribute: false,
        httpOnlyCookieAttribute: false,
      },
    },
  },
  pinia: {
    storesDirs: ['./stores/**'],
  },
})