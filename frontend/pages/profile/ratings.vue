<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '~/store/userStore'

definePageMeta({
  middleware: 'auth',
  layout: 'profile'
})

const userStore = useUserStore()

const ratedMovies = ref<{
  id: number
  title: string
  poster_path: string
  rating: number
}[]>([])

const getPosterUrl = (path: string) =>
  `https://image.tmdb.org/t/p/w500${path}`

async function fetchRatedMovies() {
  try {
    const response = await fetch(`http://localhost:8000/api/ratings/user/${userStore.user?.id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) throw new Error('Failed to fetch ratings')

    const data = await response.json()

    ratedMovies.value = data.map((entry: any) => ({
      id: entry.movie_id,
      title: entry.title,
      poster_path: entry.poster_path || '/images/placeholder_movie.jpeg',
      rating: entry.rating
    }))
  } catch (error) {
    console.error('Erreur lors du chargement des notes utilisateur :', error)
  }
}

onMounted(fetchRatedMovies)
</script>

<template>
  <div class="p-6 max-w-5xl">
    <h2 class="text-4xl font-semibold mb-10">My ratings</h2>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div v-for="movie in ratedMovies" :key="movie.id" @click="$router.push(`/movie/${movie.id}`)"
        class="relative w-[200px] h-[300px] mx-auto overflow-hidden rounded-xl shadow-md cursor-pointer transform transition-transform duration-150 active:scale-95">
        <!-- Image du film -->
        <img :src="getPosterUrl(movie.poster_path)" :alt="movie.title" class="object-cover w-full h-full" />

        <!-- Effet de fond + Titre -->
        <div class="absolute bottom-0 left-0 w-full bg-black/10 backdrop-blur-sm p-4">
          <p class="text-white text-xl mb-5 font-semibold text-center drop-shadow">
            {{ movie.title }}
          </p>
        </div>

        <!-- Étoiles -->
        <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 translate-y-full mt-2 flex gap-1">
          <Icon v-for="i in 5" :key="i" name="i-heroicons-star-solid"
            :class="i <= movie.rating ? 'text-orange-400' : 'text-gray-300'" class="w-6 h-6" />
        </div>
      </div>
    </div>
  </div>
</template>