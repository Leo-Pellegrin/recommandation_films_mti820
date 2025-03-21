export const useUserStore = defineStore('user', {
  state: () => ({
    isAuthenticated: false,
    user: null as null | { id: number; email: string; username: string },
    checkedSession: false,
  }),

  actions: {
    login(userData: { id: number; email: string; username: string }) {
      this.isAuthenticated = true;
      this.user = userData;
    },

    logout() {
      this.isAuthenticated = false;
      this.user = null;

      // Supprimer le token du cookie
      const token = useCookie('auth.token');
      token.value = null;
      window.location.reload();
    },
    async checkAuth() {
      const token = useCookie('auth.token')

      if (!token.value) {
        this.isAuthenticated = false
        this.user = null
        this.checkedSession = true
        return
      }

      if (this.checkedSession) {
        return // ✅ Évite un nouvel appel API si la session a déjà été vérifiée
      }

      try {
        const auth = useAuth()
        const session = await auth.getSession() // 🔹 Fait un seul appel à `/me`

        if (session) {
          this.isAuthenticated = true
        } else {
          this.isAuthenticated = false
          this.user = null
        }

        this.checkedSession = true // ✅ Marquer la session comme vérifiée
      } catch (error) {
        console.error("Erreur lors de la récupération de l'utilisateur :", error)
        this.isAuthenticated = false
        this.user = null
      }
    },
  },
  persist: {
    storage: piniaPluginPersistedstate.localStorage(),
  },
})