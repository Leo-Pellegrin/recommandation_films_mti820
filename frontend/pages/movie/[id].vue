<script setup lang="ts">

definePageMeta({
  middleware: 'auth',
  layout: 'default'
})


const route = useRoute()
const hoverRating = ref(0)
const userRating = ref(0)

interface Movie {
  id: number
  title: string
  backdropPath: string
  rating: number
  releaseYear: string
  runtime: string
  genres: string[]
  cast: string[]
  summary: string
  similar: { id: number; title: string; backdropPath: string }[]
}

const movie = ref<Movie | null>(null)

const TMDB_API_KEY = '166e544a3195c0c362b7c9294e90775d'
const TMDB_AUTH_HEADER = {
  Authorization: `Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNjZlNTQ0YTMxOTVjMGMzNjJiN2M5Mjk0ZTkwNzc1ZCIsIm5iZiI6MTYxMTkyMzU1NC4wMTMsInN1YiI6IjYwMTQwMDYyMTUxMWFhMDA0MDUwZTRiYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.eBu8apq8f56k4Ld1E8C3pqtN62bH3BMs2hrfjKzotQA`,
  Accept: 'application/json'
}

onMounted(async () => {
  const id = route.params.id

  console.log('Chargement du film', id)
  try {
    const res = await fetch(`https://api.themoviedb.org/3/movie/${id}?language=en-US&append_to_response=credits,similar`, {
      headers: TMDB_AUTH_HEADER
    })
    const data = await res.json()

    movie.value = {
      id: data.id,
      title: data.title,
      backdropPath: data.backdrop_path
        ? `https://image.tmdb.org/t/p/w780${data.backdrop_path}`
        : '/images/placeholder_backdrop.jpeg',
      rating: data.vote_average,
      releaseYear: data.release_date?.split('-')[0] || 'N/A',
      runtime: data.runtime ? `${Math.floor(data.runtime / 60)}h ${data.runtime % 60}m` : 'N/A',
      genres: data.genres.map((g: any) => g.name),
      cast: data.credits?.cast.slice(0, 3).map((a: any) => a.name) || [],
      summary: data.overview,
      similar: data.similar?.results.slice(0, 10).map((m: any) => ({
        id: m.id,
        title: m.title,
        backdropPath: m.backdrop_path
          ? `https://image.tmdb.org/t/p/w780${m.backdrop_path}`
          : '/images/placeholder_backdrop.jpeg'
      })) || []
    }
  } catch (e) {
    console.error('Erreur de chargement du film', e)
  }
})
</script>

<template>
  <div v-if="movie" class="bg-black text-white min-h-screen p-10">
    <div class="flex flex-col lg:flex-row gap-10">
      <!-- Backdrop image -->
      <img
        :src="movie.backdropPath"
        :alt="movie.title"
        class="w-full lg:w-[60%] rounded-xl shadow-lg object-cover"
      />

      <!-- Movie details -->
      <div class="flex-1 flex flex-col justify-between">
        <div>
          <h1 class="text-5xl font-bold mb-4">{{ movie.title }}</h1>

          <button class="flex items-center gap-2 bg-white text-black font-semibold px-5 py-2 rounded-full mb-6">
            <span class="bg-orange-400 text-white rounded-full w-6 h-6 flex items-center justify-center">▶</span>
            PLAY
          </button>

          <div class="flex items-center mb-4">
            <span class="mr-2">Rate this movie:</span>
            <div class="flex text-orange-400 text-xl">
             <div class="flex items-center space-x-1">
            <UIcon
      v-for="i in 5"
      :key="i"
      @mouseover="hoverRating = i"
      @mouseleave="hoverRating = 0"
      @click="userRating = i"
      :name="(hoverRating || userRating) >= i
        ? 'material-symbols-kid-star'
        : 'material-symbols-kid-star-outline-sharp'"
      class="text-2xl text-orange-400 cursor-pointer transition-colors"
    />
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
        <MovieMarquee
          :key="movie.id"
          :title="'More movies like this one'"
          :movies="movie.similar.map(similar => ({
            id: similar.id,
            title: similar.title,
            posterPath: similar.backdropPath
          }))"
        />
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
