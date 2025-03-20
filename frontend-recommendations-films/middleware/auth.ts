import { defineNuxtRouteMiddleware, navigateTo } from '#app'
import { useUserStore } from '~/store/userStore'

export default defineNuxtRouteMiddleware(() => {
  const userStore = useUserStore()
  
  if (!userStore.isAuthenticated) {
    return navigateTo('/login')
  }
})