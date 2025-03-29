<script setup lang="ts">
import { useUserStore } from '~/store/userStore'
import { ref, onMounted } from 'vue'

definePageMeta({
  middleware: 'auth',
  layout: 'profile'
})

const userStore = useUserStore()
const selectedGenres = ref<string[]>([])
const selectedActors = ref<string[]>([])
const selectedMovies = ref<{ movie_id: number; title: string }[]>([])

async function fetchPreferences() {
  const userId = userStore.user?.id
  if (!userId) return

  const [genresRes, actorsRes, moviesRes] = await Promise.all([
    fetch(`http://localhost:8000/api/preferences/${userId}/genres`),
    fetch(`http://localhost:8000/api/preferences/${userId}/actors`),
    fetch(`http://localhost:8000/api/preferences/${userId}/favorites/movies`)
  ])

  selectedGenres.value = (await genresRes.json()).preferred_genres || []
  selectedActors.value = (await actorsRes.json()).preferred_actors || []
  selectedMovies.value = await moviesRes.json()
}

const removeGenre = async (index: number) => {
  const genre = selectedGenres.value[index]
  selectedGenres.value.splice(index, 1)

  await fetch(`http://localhost:8000/api/preferences/${userStore.user?.id}/genres/${genre}`, {
    method: 'DELETE'
  })
}

const removeActor = async (index: number) => {
  const actor = selectedActors.value[index]
  selectedActors.value.splice(index, 1)

  await fetch(`http://localhost:8000/api/preferences/${userStore.user?.id}/actors/${actor}`, {
    method: 'DELETE'
  })
}

const removeMovie = async (index: number) => {
  const movie = selectedMovies.value[index]
  selectedMovies.value.splice(index, 1)

  await fetch(`http://localhost:8000/api/preferences/${userStore.user?.id}/favorites/movies/${movie.movie_id}`, {
    method: 'DELETE'
  })
}

onMounted(fetchPreferences)
</script>
<template>
  <div class="p-6 space-y-10 max-w-3xl">
    <h2 class="text-4xl font-semibold">Your preferences</h2>

    <!-- Favorite genres -->
    <div class="flex flex-col gap-3">
      <div class="flex items-center justify-between">
        <label class="text-2xl font-medium">Favorite genres</label>
        <UButton icon="i-heroicons-pencil-square" class="text-black" size='xl' @click="$router.push('/edit-preferences/genres')">
          Edit genres
        </UButton>
      </div>
      <div class="flex flex-wrap gap-2 p-3 rounded-lg bg-zinc-800">
        <UBadge v-for="(genre, index) in selectedGenres" :key="genre"
          class="bg-orange-400  px-3 py-1 rounded-full text-lg">
          {{ genre }}
        </UBadge>
      </div>
    </div>

    <!-- Favorite actors -->
    <div class="flex flex-col gap-3">
      <div class="flex items-center justify-between">
        <label class="text-2xl font-medium">Favorite actors</label>
        <UButton class="text-black" size='xl' icon="i-heroicons-pencil-square" @click="$router.push('/edit-preferences/actors')">
          Edit actors
        </UButton>
      </div>
      <div class="flex flex-wrap gap-2 p-3 rounded-lg bg-zinc-800">
        <UBadge v-for="(actor, index) in selectedActors" :key="actor"
          class="bg-orange-400 px-3 py-1 rounded-full text-lg">
          {{ actor }}
        </UBadge>
      </div>
    </div>

    <!-- Favorite movies -->
    <div class="flex flex-col gap-3">
      <div class="flex items-center justify-between">
        <label class="text-2xl font-medium">Favorite movies</label>
        <UButton icon="i-heroicons-pencil-square" class="text-black" size='xl' @click="$router.push('/edit-preferences/movies')">
          Edit movies
        </UButton>
      </div>
      <div class="flex flex-wrap gap-2 p-3 rounded-lg bg-zinc-800">
        <UBadge v-for="(movie, index) in selectedMovies" :key="movie.movie_id"
          class="bg-orange-400  px-3 py-1 rounded-full text-lg">
          {{ movie.title }}
        </UBadge>
      </div>
    </div>
  </div>
</template>