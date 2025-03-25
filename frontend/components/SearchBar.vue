<script setup lang="ts">
const searchTerm = ref('')
const results = ref([])
const loading = ref(false)

// Fonction de recherche
async function searchMovies(query: string) {
  if (!query) return

  loading.value = true
  try {
    const res = await fetch(`https://api.themoviedb.org/3/search/movie?query=${encodeURIComponent(query)}&language=en-US&page=1`, {
      headers: {
        Authorization: `Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNjZlNTQ0YTMxOTVjMGMzNjJiN2M5Mjk0ZTkwNzc1ZCIsIm5iZiI6MTYxMTkyMzU1NC4wMTMsInN1YiI6IjYwMTQwMDYyMTUxMWFhMDA0MDUwZTRiYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.eBu8apq8f56k4Ld1E8C3pqtN62bH3BMs2hrfjKzotQA`,
        Accept: 'application/json'
      }
    })
    const data = await res.json()
    results.value = (data.results || []).map((movie: any) => ({
      id: movie.id,
      label: movie.title,
      suffix: movie.release_date?.split('-')[0] || '',
      avatar: {
        src: movie.poster_path
          ? `https://image.tmdb.org/t/p/w92${movie.poster_path}`
          : '/images/placeholder_movie.jpeg'
      }
    }))
  } catch (e) {
    console.error('Erreur de recherche :', e)
  } finally {
    loading.value = false
  }
}

// Requête déclenchée automatiquement quand on tape
watch(searchTerm, (query) => {
  if (query.trim().length >= 2) {
    searchMovies(query)
  } else {
    results.value = []
  }
})

const groups = computed(() => [{
  id: 'movies',
  label: searchTerm.value ? `Movies matching “${searchTerm.value}”...` : 'Movies',
  items: results.value
}])

const emit = defineEmits<{ close: [boolean] }>()
</script>

<template>
  <UModal :title="'Search for a movie'" class="bg-zinc-900" :close="{ onClick: () => emit('close', false) }" :ui="{overlay: 'fixed inset-0 bg-(--ui-bg-elevated)/75'}"> 
    <template #content>
    <UCommandPalette
        v-model:search-term="searchTerm"
        :loading="loading"
        :groups="groups"
        placeholder="Search for a movie..."
        class="bg-zinc-900 shadow-2xl rounded-xl text-white"
        @update:model-value="(item) => {
            navigateTo(`/movie/${item.id}`)
            emit('close', false)
        }"
        />
    </template>
  </UModal>
</template>

<style scoped>

</style>
