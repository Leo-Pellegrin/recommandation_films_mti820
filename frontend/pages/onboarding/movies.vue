<script setup lang="ts">
import { useMovies } from '~/composables/useMovies'
import { useUserStore } from '~/store/userStore'
import { onMounted, computed } from 'vue'

definePageMeta({
  middleware: 'auth',
  layout: 'auth',
  alias: ['/edit-preferences/movies']  // <- permet d'accéder à cette page avec cette URL
})

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isEditMode = computed(() => route.path.includes('/edit-preferences'))

const {
  selectedMovies,
  toggleMovie,
  displayedMovies,
  searchQuery,
  fetchMovies
} = useMovies()

function nextStep() {
  if (isEditMode.value) {
    router.push('/profile/preferences') // ou une autre page
  } else {
    router.push('/onboarding/moviesratings')
  }
}

async function fetchExistingPreferences() {
  const res = await fetch(`http://localhost:8000/api/preferences/${userStore.user?.id}/favorites/movies`)
  const data = await res.json()
  data.forEach((movie: any) => {
    toggleMovie({
      id: movie.movie_id,
      title: movie.title,
      posterPath: movie.poster_path
    })
  })
}

onMounted(async () => {
  await fetchMovies()
  if (isEditMode.value) {
    await fetchExistingPreferences()
  }
})

async function submitSelection() {
  try {
    const response = await fetch(
      `http://localhost:8000/api/preferences/${userStore.user?.id}/favorites/movies/batch`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          movie_ids: selectedMovies.value.map((movie) => movie.id)
        })
      }
    )

    if (response.ok) {
      if (isEditMode.value) {
        router.push("/profile/preferences")
      }
      else {
        nextStep()
      }
    } else {
      console.error(`Erreur : statut ${response.status}`)
    }
  } catch (error) {
    console.error('Erreur lors de l\'envoi des films sélectionnés :', error)
  }
}
</script>
<template>
  <div class="min-h-screen bg-black text-white flex flex-col p-12">
    <h1 class="flex justify-center mt-10 text-5xl font-extrabold mb-6">
      {{ isEditMode ? 'Edit your favorite movies' : 'Select your favorite movies' }}
    </h1>

    <UInput v-model="searchQuery" placeholder="Search movies..." :ui="{ base: 'text-lg p-4' }"
      class="w-2/3 text-2xl p-5 mt-10 mx-auto bg-gray-800 text-black rounded-2xl shadow-lg" />

    <div v-if="selectedMovies.length" class="grid grid-cols-6 gap-6 mt-8">
      <div v-for="movie in selectedMovies" :key="movie.id">
        <UButton @click="toggleMovie(movie)"
          class="w-48 h-15 flex items-center justify-center rounded-2xl bg-orange-400 text-white shadow-xl"
          trailing-icon="mdi-close">
          <span class="text-xl font-semibold">{{ movie.title }}</span>
        </UButton>
      </div>
    </div>

    <div class="grid grid-cols-6 gap-10 mt-12">
      <div v-for="movie in displayedMovies.slice(0, 12)" :key="movie.id">
        <UButton @click="toggleMovie(movie)"
          class="w-48 h-48 flex flex-col items-center justify-center rounded-2xl text-white shadow-xl hover:bg-orange-400 transition-all"
          :class="selectedMovies.some(m => m.id === movie.id) ? 'bg-orange-400 border-orange-500' : ''">
          <img :src="movie.posterPath || '/placeholder.webp'" class="w-28 h-28 rounded-xl object-cover"
            alt="Movie poster" />
          <span class="mt-2 text-xl font-semibold text-center">{{ movie.title }}</span>
        </UButton>
      </div>
    </div>

    <div class="flex justify-center mt-16">
      <UButton @click="submitSelection"
        class="mt-10 text-xl px-8 py-4 bg-orange-500 hover:bg-orange-600 text-white rounded-xl">
        {{ isEditMode ? 'Save changes' : 'Continue →' }}
      </UButton>
    </div>
  </div>
</template>