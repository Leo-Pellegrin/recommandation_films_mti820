<script setup lang="ts">
import { useTopRatedMovies } from '~/composables/useTopRatedMovies'

definePageMeta({
  middleware: 'auth',
  layout: 'default'
})

const { topRatedMovies, loading } = useTopRatedMovies()
</script>

<template>
  <div class="p-6 bg-black min-h-screen text-white ml-6">
    <h1 class="text-4xl font-bold mb-8">Recommended Movies</h1>

    <div v-if="loading" class="text-center text-lg">Loading...</div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-10 mx-auto">
      <MovieCard v-for="movie in topRatedMovies" :key="movie.movie_id" :id="movie.movie_id" :title="movie.title"
        :posterPath="movie.posterPath" size="large" />
    </div>
  </div>
</template>

<style lang="css" scoped>
.no-scrollbar {
  -ms-overflow-style: none;
  /* IE and Edge */
  scrollbar-width: none;
  /* Firefox */
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
  /* Chrome, Safari and Opera */
}
</style>