<script setup lang="ts">
import { useAuth } from '#imports'
import { useUserStore } from '~/store/userStore'

const userStore = useUserStore()

onMounted(async () => {
  await userStore.checkAuth();
});

const { status } = useAuth()

async function logout() {
  console.log("Logging out")

  try {
    // ✅ Supprimer le token stocké en cookie
    const token = useCookie('auth.token')
    token.value = null

    // ✅ Mettre à jour le store utilisateur
    await userStore.logout()

    // ✅ Redirection vers la page de connexion après logout
    navigateTo('/auth/login')

  } catch (error) {
    console.error("Erreur lors de la déconnexion:", error)
  }
}

</script>

<template>
  <div>
    <AppBar />
    <main class="p-4 bg-black text-white ">
      <slot />
    </main>
  </div>
</template>
