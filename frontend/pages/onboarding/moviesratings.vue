<script setup lang="ts">
import { useUserStore } from '~/store/userStore'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

definePageMeta({
  middleware: 'auth',
  layout: 'auth'
})

const router = useRouter()
const userStore = useUserStore()

interface Movie {
  movie_id: number
  title: string
  poster_path: string
  year?: number
  genres?: string[]
}

const favoriteMovies = ref<Movie[]>([])
const ratings = ref<{ movie_id: number; rating: number }[]>([])

// Gère les étoiles survolées individuellement
const hoverRatings = ref<{ [key: number]: number }>({})
const userRatings = ref<{ [key: number]: number }>({})

function setRating(movieId: number, value: number) {
  userRatings.value[movieId] = value
  const existing = ratings.value.find(r => r.movie_id === movieId)
  if (existing) {
    existing.rating = value
  } else {
    ratings.value.push({ movie_id: movieId, rating: value })
  }
}

const gridCols = ref('')


onMounted(async () => {
  favoriteMovies.value = await getFavoritesMovies()
  const count = favoriteMovies.value.length

  const cols = Math.min(count, 5)
  console.log(cols)

  gridCols.value = `grid-cols-${cols > 0 ? cols : 1}`
  console.log(gridCols.value)
})

async function getFavoritesMovies() {
  try {
    const response = await fetch(`http://localhost:8000/api/preferences/${userStore.user?.id}/favorites/movies`)
    if (!response.ok) throw new Error(`Erreur serveur: ${response.status}`)
    return await response.json()
  } catch (error) {
    console.error("Erreur lors de la récupération des films favoris :", error)
    return []
  }
}

async function submitRatings() {
  if (ratings.value.length === 0) {
    console.warn("Aucune note sélectionnée")
    return
  }

  try {
    const response = await fetch(`http://localhost:8000/api/ratings/user/${userStore.user?.id}/ratings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(ratings.value.map(r => ({
        ...r,
        timestamp: new Date().toISOString()
      })))
    })

    if (response.ok) {
        finishOnboarding()
    } else {
      console.error('Erreur serveur:', await response.text())
    }
  } catch (err) {
    console.error('Erreur d\'envoi des notes:', err)
  }
}

function finishOnboarding(){
    router.push('/onboarding/finish')
}
</script>

<template>
  <div class="min-h-screen bg-black text-white p-10">
    <h1 class="text-4xl font-bold text-center mb-6 mt-20">Rate your favorite movies</h1>

    <div class="grid gap-8 mt-20" :class="gridCols">
      <div
        v-for="movie in favoriteMovies"
        :key="movie.movie_id"
        class="bg-gray-900 p-4 rounded-xl shadow-md flex flex-col items-center"
      >
        <img :src="movie.poster_path" class="w-32 h-48 object-cover rounded" />
        <h2 class="text-lg font-semibold mt-3 text-center">{{ movie.title }}</h2>

        <!-- Notation avec étoiles -->
        <div class="flex mt-4 gap-1">
          <Icon
            v-for="i in 5"
            :key="i"
            @mouseover="hoverRatings[movie.movie_id] = i"
            @mouseleave="hoverRatings[movie.movie_id] = 0"
            @click="setRating(movie.movie_id, i)"
            :name="(hoverRatings[movie.movie_id] || userRatings[movie.movie_id] || 0) >= i
              ? 'material-symbols-kid-star'
              : 'material-symbols-kid-star-outline-sharp'"
            class="text-2xl text-orange-400 cursor-pointer transition-colors"
          />
        </div>
      </div>
    </div>

    <div class="flex justify-center mt-10">
      <UButton
        class="px-10 py-4 mt-10 text-xl bg-orange-500 hover:bg-orange-700 text-white rounded-xl"
        @click="submitRatings"
      >
        Submit Ratings
      </UButton>
    </div>
  </div>
</template>