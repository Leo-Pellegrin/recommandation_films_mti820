import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    isAuthenticated: false, // Ajoute cette variable si elle manque
  }),
  actions: {
    login() {
      this.isAuthenticated = true
    },
    logout() {
      this.isAuthenticated = false
    },
  },
})