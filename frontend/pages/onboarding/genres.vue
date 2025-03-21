<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useGenres } from '~/composables/useGenres'
import { useUserStore } from '~/store/userStore'

const userStore = useUserStore()
const user = ref({ id: 0, email: '', username: '' })
const router = useRouter()

function finishOnboarding() {
  router.push('/onboarding/actors')
}

onMounted(async () => {
  await userStore.checkAuth()
  console.log('UserStore:', userStore.user)
  if (userStore.isAuthenticated) { // ✅ Vérifie si l'utilisateur est connecté
    user.value = {
      id: userStore.user?.id ?? 0,
      email: userStore.user?.email ?? '',
      username: userStore.user?.username ?? ''
    }

    console.log('User:', user.value)
  }
}
)

definePageMeta({
  middleware: 'auth',
  layout: 'auth'
})

const { genres, selectedGenres, toggleGenre } = useGenres()

// Bouton de validation
function submitSelection() {
  console.log('Genres sélectionnés :', selectedGenres.value)
  // Envoyer a l'api les genres sélectionnés

  finishOnboarding()
}

</script>

<template>
  <div class="flex flex-col items-center space-y-6">
    <h1 class="text-5xl font-bold text-white">Welcome {{ userStore.user?.username }}, let's get you started.</h1>
    <h2 class="text-3xl font-bold text-white">Select your favorite genres</h2>

    <div class="grid grid-cols-4 gap-20 mt-16">
      <UButton v-for="genre in genres" :key="genre"
        :ui="{ base: 'w-60 h-18 px-6 py-3 text-2xl font-medium mx-auto rounded-xl transition-all', }"
        class="border-2 flex justify-center items-center hover:bg-orange-400 hover:text-white hover:border-orange-500"
        :class="selectedGenres.includes(genre) ? 'bg-orange-400 text-white border-orange-500' : 'bg-white text-black'"
        @click="toggleGenre(genre)">
        {{ genre }}
      </UButton>
    </div>

    <UButton
      class="w-60 h-18 text-2xl flex justify-center items-center mt-16 bg-orange-400 hover:bg-orange-600 text-white px-6 py-3 rounded-xl"
      @click="submitSelection">
      Continue →
    </UButton>
  </div>
</template>