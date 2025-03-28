<script setup lang="ts">
import { useTopRatedMovies } from '~/composables/useTopRatedMovies'

const { movieCategories } = useTopRatedMovies()

definePageMeta({
  middleware: 'auth',
  layout: 'default'
})

</script>

<template>
  <div class="p-6 bg-black min-h-screen no-scrollbar">
    <MovieMarquee v-for="(movieList, genre) in movieCategories" :key="genre" :title="genre" :movies="movieList" />
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