<template>
  <div class="mb-10">
    <h2 class="text-3xl font-bold text-white mb-8">{{ title }}</h2>

    <div class="overflow-x-auto no-scrollbar">
      <div class="flex space-x-10 w-max">
        <MovieCard v-for="movie in movies" :key="movie.id" :id="movie.id" :title="movie.title"
          :posterPath="movie.posterPath" :score="movie.score" size="medium" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  movies: {
    id: number
    title: string
    posterPath: string
    score?: number
  }[]
}>()
</script>

<style scoped>
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