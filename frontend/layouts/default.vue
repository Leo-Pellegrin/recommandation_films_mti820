<script setup lang="ts">
import { useAuth } from '#imports'
import { useUserStore } from '~/store/userStore'

const userStore = useUserStore()

onMounted(async () => {
  await userStore.checkAuth();
});

const { status } = useAuth()
</script>

<template>
  <div>
    <header v-if="!$route.path.startsWith('/auth')">
      <nav class="p-4 bg-gray-800 text-white flex justify-between">
        <NuxtLink to="/" class="font-bold">Accueil</NuxtLink>
        <NuxtLink to="/profile/preferences" v-if="status === 'authenticated'">Profil</NuxtLink>
        <NuxtLink to="/auth/login" v-else>Connexion</NuxtLink>
      </nav>
    </header>

    <main class="p-4">
      <slot /> <!-- 🔹 Affiche la page actuelle ici -->
    </main>
  </div>
</template>

