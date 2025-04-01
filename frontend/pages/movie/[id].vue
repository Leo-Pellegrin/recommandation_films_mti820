<script setup lang="ts">
import { useUserStore } from '~/store/userStore'

definePageMeta({
  middleware: 'auth',
  layout: 'default'
})

const route = useRoute()
const userStore = useUserStore()
const hoverRating = ref(0)
const userRating = ref(0)
const toast = useToast()

interface SimilarMovie {
  id: number
  title: string
  backdropPath: string
  score: number
}

interface Movie {
  id: number
  title: string
  backdropPath: string
  rating: number | null
  releaseYear: string
  runtime: string
  genres: string[]
  cast: string[]
  summary: string
  similar: SimilarMovie[]
}

const movie = ref<Movie | null>(null)

onMounted(async () => {
  const id = route.params.id
  try {
    const res = await fetch(`http://localhost:8000/api/movies/movie/${id}?user_id=${userStore.user?.id}`)
    const data = await res.json()

    movie.value = {
      id: data.movie_id,
      title: data.title,
      backdropPath: data.backdrop_path
        ? `https://image.tmdb.org/t/p/w780${data.backdrop_path}`
        : '/images/placeholder_backdrop.jpeg',
      rating: data.rating,
      releaseYear: data.release_year || 'N/A',
      runtime: data.runtime ? `${Math.floor(data.runtime / 60)}h ${data.runtime % 60}m` : 'N/A',
      genres: data.genres,
      cast: data.cast,
      summary: data.summary,
      similar: []
    }

    if (data.rating) userRating.value = data.rating

    // Appel des recommandations item-based
    const recoRes = await fetch(`http://localhost:8000/api/recommendations/item/movies/${movie.value.id}`)
    const recoData = await recoRes.json()

    if (Array.isArray(recoData)) {
      movie.value.similar = recoData
        .map((m: any) => ({
          id: m.movie_id,
          title: m.title,
          backdropPath: m.posterPath
            ? `https://image.tmdb.org/t/p/w780${m.posterPath}`
            : '/images/placeholder_movie.jpeg',
          score: m.preferenceScore
        }))
        .sort((a, b) => b.score - a.score) // ⬅️ tri décroissant
    }
  } catch (error) {
    console.error('Erreur lors de la récupération des données du film ou des recommandations :', error)
  }
})

async function submitRating(value: number) {
  try {
    const response = await fetch(`http://localhost:8000/api/ratings/user/${userStore.user?.id}/rating`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        movie_id: movie.value?.id,
        rating: value,
        timestamp: new Date().toISOString()
      })
    })

    if (response.ok) {
      toast.add({ title: 'Success', description: 'Rating saved', color: 'success' })
    } else {
      console.error("❌ Erreur serveur:", await response.text())
    }
  } catch (err) {
    console.error("❌ Erreur lors de l’enregistrement:", err)
  }
}
</script>

<template>
  <div v-if="movie" class="bg-black text-white min-h-screen p-10">
    <div class="flex flex-col lg:flex-row gap-10">
      <!-- Backdrop image -->
      <img :src="movie.backdropPath" :alt="movie.title" class="w-full lg:w-[60%] rounded-xl shadow-lg object-cover" />

      <!-- Movie details -->
      <div class="flex-1 flex flex-col justify-between">
        <div>
          <h1 class="text-5xl font-bold mb-4">{{ movie.title }}</h1>

          <button class="flex items-center gap-2 bg-white text-black font-semibold px-5 py-2 rounded-full mb-6">
            <span class="bg-orange-400 text-white rounded-full w-6 h-6 flex items-center justify-center">▶</span>
            PLAY
          </button>

          <!-- Notation -->
          <div class="flex items-center mb-4">
            <span class="mr-2">Rate this movie:</span>
            <div class="flex text-orange-400 text-xl">
              <div class="flex items-center space-x-1">
                <UIcon v-for="i in 5" :key="i" @mouseover="hoverRating = i" @mouseleave="hoverRating = 0" @click="() => {
                  userRating = i
                  submitRating(i)
                }" :name="(hoverRating || userRating) >= i
                  ? 'material-symbols-kid-star'
                  : 'material-symbols-kid-star-outline-sharp'"
                  class="text-2xl text-orange-400 cursor-pointer transition-colors" />
              </div>
            </div>
          </div>

          <p class="mb-2 text-lg text-gray-300">{{ movie.releaseYear }} | {{ movie.runtime }}</p>
          <p class="mb-2 text-lg text-gray-300">Genres: {{ movie.genres.join(', ') }}</p>
          <p class="mb-4 text-lg text-gray-300">Cast: {{ movie.cast.join(', ') }}</p>

          <p class="text-lg text-gray-100">{{ movie.summary }}</p>
        </div>
      </div>
    </div>

    <!-- Similar Movies -->
    <div class="mt-16">
      <div class="flex gap-4 overflow-x-auto no-scrollbar py-4">
        <MovieMarquee :key="movie.id" :title="'More movies like this one'" :movies="movie.similar.map(similar => ({
          id: similar.id,
          title: similar.title,
          posterPath: similar.backdropPath,
          score: similar.score
        }))" />
      </div>
    </div>
  </div>
</template>

<style>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}

.no-scrollbar {
  scrollbar-width: none;
}
</style>
