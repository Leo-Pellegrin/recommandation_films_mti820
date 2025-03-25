<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
  layout: 'profile'
})

const movieIds = [
  { id: 916224, rating: 4 }, 
  { id: 238, rating: 5 },    
  { id: 550, rating: 3 }, 
]

const ratedMovies = ref<
  {
    id: number
    title: string
    poster_path: string
    rating: number
  }[]
>([])

const getPosterUrl = (path: string) =>
  `https://image.tmdb.org/t/p/w500${path}`

const fetchMovie = async (id: number) => {
  const apiKey = '166e544a3195c0c362b7c9294e90775d'
  const res = await fetch(`https://api.themoviedb.org/3/movie/${id}?api_key=${apiKey}`)
  if (!res.ok) throw new Error('Movie not found')
  return res.json()
}

onMounted(async () => {
  for (const entry of movieIds) {
    try {
      const data = await fetchMovie(entry.id)
      ratedMovies.value.push({
        id: data.id,
        title: data.title,
        poster_path: data.poster_path,
        rating: entry.rating
      })
    } catch (e) {
      console.error('Error fetching movie:', e)
    }
  }
})
</script>

<template>
  <div class="p-6 max-w-5xl">
    <h2 class="text-4xl font-semibold mb-10">My ratings</h2>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div
        v-for="movie in ratedMovies"
        :key="movie.id"
        class="relative w-[200px] h-[300px] mx-auto overflow-hidden rounded-xl shadow-md"
      >
        <!-- Image du film -->
        <img
          :src="getPosterUrl(movie.poster_path)"
          :alt="movie.title"
          class="object-cover w-full h-full"
          @click="$router.push(`/movie/${movie.id}`)"
        />

        <!-- Effet de fond + Titre -->
        <div class="absolute bottom-0 left-0 w-full bg-black/1 backdrop-blur-sm p-4">
          <p class="text-white text-xl mb-4 font-semibold text-center drop-shadow">
            {{ movie.title }}
          </p>
        </div>

        <!-- Étoiles -->
        <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 translate-y-full mt-2 flex gap-1">
          <Icon
            v-for="i in 5"
            :key="i"
            name="i-heroicons-star-solid"
            :class="i <= movie.rating ? 'text-orange-400' : 'text-gray-300'"
            class="w-6 h-6"
          />
        </div>
      </div>
    </div>
  </div>
</template>
