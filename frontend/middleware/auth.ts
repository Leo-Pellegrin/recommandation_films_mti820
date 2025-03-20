export default defineNuxtRouteMiddleware(async () => {
  const { status } = useAuth()

  if (status.value !== 'authenticated') {
    return navigateTo('/auth/login')
  }
})