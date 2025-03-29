<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useGenres } from '~/composables/useGenres'
import { useUserStore } from '~/store/userStore'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// Détection du mode édition
const isEditMode = computed(() => route.path.includes('/edit-preferences'))

const user = ref({ id: 0, email: '', username: '' })

definePageMeta({
  middleware: 'auth',
  layout: 'auth',
  alias: ['/edit-preferences/genres'] 
})

const { genres, selectedGenres, toggleGenre } = useGenres()

// Navigation vers l’étape suivante si onboarding
function nextOnboarding() {
  router.push('/onboarding/actors')
}

onMounted(async () => {
  await userStore.checkAuth()

  if (userStore.isAuthenticated) {
    user.value = {
      id: userStore.user?.id ?? 0,
      email: userStore.user?.email ?? '',
      username: userStore.user?.username ?? ''
    }

    // Si en édition, charger les préférences actuelles
    if (isEditMode.value && userStore.user?.id) {
      try {
        const res = await fetch(`http://localhost:8000/api/preferences/${userStore.user.id}/genres`)
        const data = await res.json()
        selectedGenres.value = data.preferred_genres || []
      } catch (e) {
        console.error("Erreur lors du chargement des genres existants :", e)
      }
    }
  }
})

// Envoi des préférences au backend
async function submitSelection() {
  console.log('Genres sélectionnés :', selectedGenres.value)

  try {
    const urlPreferencesGenre = `http://localhost:8000/api/preferences/${userStore.user?.id}/genres`

    const response = await fetch(urlPreferencesGenre, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ genres: selectedGenres.value })
    })

    if (response.ok) {
      if (!isEditMode.value) {
        nextOnboarding()
      } else {
        
        console.log("Genres mis à jour avec succès")
        router.push("/profile/preferences")
      }
    } else {
      console.error(`Erreur : statut ${response.status}`)
    }
  } catch (error) {
    console.error("Erreur lors de l'envoi des genres sélectionnés :", error)
  }
}
</script>

<template>
  <div class="flex flex-col items-center space-y-6">
    <h1 class="text-5xl font-bold text-white">
      {{ isEditMode ? 'Edit your preferences' : `Welcome ${userStore.user?.username}, let's get you started.` }}
    </h1>
    <h2 class="text-3xl font-bold text-white">
      {{ isEditMode ? 'Update your favorite genres' : 'Select your favorite genres' }}
    </h2>

    <div class="grid grid-cols-4 gap-20 mt-16">
      <UButton
        v-for="genre in genres"
        :key="genre"
        :ui="{ base: 'w-60 h-18 px-6 py-3 text-2xl font-medium mx-auto rounded-xl transition-all', }"
        class="border-2 flex justify-center items-center hover:bg-orange-400 hover:text-white hover:border-orange-500"
        :class="selectedGenres.includes(genre)
          ? 'bg-orange-400 text-white border-orange-500'
          : 'bg-white text-black'"
        @click="toggleGenre(genre)"
      >
        {{ genre }}
      </UButton>
    </div>

    <UButton
      class="w-60 h-18 text-2xl flex justify-center items-center mt-16 bg-orange-400 hover:bg-orange-600 text-white px-6 py-3 rounded-xl"
      @click="submitSelection"
    >
      {{ isEditMode ? 'Save changes' : 'Continue →' }}
    </UButton>
  </div>
</template>