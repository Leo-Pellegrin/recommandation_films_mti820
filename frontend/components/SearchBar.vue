<script setup lang="ts">
import { ref, watch, computed } from 'vue'

interface CommandPaletteItem {
  id?: number | string
  label: string
  suffix?: string
  avatar?: {
    src: string
  }
}

const searchQuery = ref('')
const loading = ref(false)
const results = ref<CommandPaletteItem[]>([])

const emit = defineEmits<{ close: [boolean] }>()

async function searchMovies(query: string) {
  try {
    const response = await fetch(`http://localhost:8000/api/movies/search/${encodeURIComponent(query)}`)
    const data = await response.json()
    results.value = data.map((movie: any) => ({
      id: movie.movie_id,
      label: movie.title,
      avatar: {
        src: movie.poster_path ?? '/images/placeholder_movie.jpeg'
      }
    }))
  } catch (error) {
    console.error('Erreur lors de la recherche de films :', error)
  }
}

watch(searchQuery, async (query) => {
  if (query.trim().length >= 2) {
    loading.value = true
    await searchMovies(query)
    loading.value = false
  } else {
    results.value = []
  }
})

const groups = computed(() => [{
  id: 'movies',
  label: searchQuery.value ? `Movies matching “${searchQuery.value}”...` : 'Movies',
  items: results.value
}])
</script>

<template>
  <UModal :title="'Search for a movie'" class="bg-zinc-900" :close="{ onClick: () => emit('close', false) }"
    :ui="{ overlay: 'fixed inset-0 bg-(--ui-bg-elevated)/75' }">
    <template #content>
      <UCommandPalette v-model:search-term="searchQuery" :loading="loading" :groups="groups"
        placeholder="Search for a movie..." class="bg-zinc-900 shadow-2xl rounded-xl text-white" @update:model-value="(item: any) => {
          navigateTo(`/movie/${item.id}`)
          emit('close', false)
        }">
        <template #item-leading="{ item }">
          <img :src="item.avatar?.src || '/images/placeholder_movie.jpeg'" alt="Movie poster"
            class="w-32 h-48 rounded object-cover" />
        </template>
      </UCommandPalette>
    </template>
  </UModal>
</template>