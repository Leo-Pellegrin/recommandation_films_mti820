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
    <header v-if="!$route.path.startsWith('/auth')">
      <nav class="p-4 bg-gray-800 text-white flex justify-between">
        <NuxtLink to="/" class="font-bold">Accueil</NuxtLink>
        <NuxtLink to="/profile/preferences" v-if="status === 'authenticated'">Profil</NuxtLink>
        <UButton @click="logout" v-if="status === 'authenticated'" >Déconnexion</UButton>
        <NuxtLink to="/auth/login" v-else>Connexion</NuxtLink>
      </nav>
    </header>

    <main class="p-4">
      <slot /> <!-- 🔹 Affiche la page actuelle ici -->
    </main>
  </div>
</template>
