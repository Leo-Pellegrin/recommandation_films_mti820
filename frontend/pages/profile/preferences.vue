<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
  layout: 'profile'
})

const genreOptions = ['Action', 'Comedy', 'Drama', 'Romance', 'Anime', 'Sci-Fi']
const movieOptions = ['D1', 'D2', 'D3', 'D4']
const actorOptions = ['A1', 'A2', 'A3', 'A4']

const selectedGenres = ref(['Action', 'Anime', 'Romance'])
const selectedMovies = ref(['D1', 'D2', 'D3'])
const selectedActors = ref(['A1', 'A2', 'A3'])

const removeGenre = (index: number) => selectedGenres.value.splice(index, 1)
const removeMovie = (index: number) => selectedMovies.value.splice(index, 1)
const removeActor = (index: number) => selectedActors.value.splice(index, 1)
</script>

<template>
  <div class="p-6 space-y-6 max-w-3xl">
    <h2 class="text-4xl font-semibold">Your preferences</h2>

    <!-- Favorite genres -->
    <div class="flex flex-col">
      <label class="text-2xl font-medium">Your favorite genres</label>
      <USelectMenu v-model="selectedGenres" :options="genreOptions" multiple placeholder="Select genres" class="mt-2">
        <template #default>
          <div class="flex flex-wrap gap-2 p-3 rounded-lg">
            <UBadge v-for="(genre, index) in selectedGenres" :key="index"
              class="bg-orange-400 text-lg text-white flex items-center gap-1 px-3 mx-2 py-1 rounded-full">
              {{ genre }}
              <UButton icon="i-heroicons-x-mark" variant="link" color="primary" size="xl"
                @click.stop="removeGenre(index)" />
            </UBadge>
          </div>
        </template>
      </USelectMenu>
    </div>

    <!-- Favorite actors -->
    <div class="flex flex-col">
      <label class="text-2xl font-medium">Your favorite actors/actress</label>
      <USelectMenu v-model="selectedActors" :options="actorOptions" multiple placeholder="Select actors" class="mt-2">
        <template #default>
          <div class="flex flex-wrap gap-2 p-3 rounded-lg">
            <UBadge v-for="(actor, index) in selectedActors" :key="index"
              class="bg-orange-400 text-lg text-white flex items-center gap-1 px-3 mx-2 py-1 rounded-full">
              {{ actor }}
              <UButton icon="i-heroicons-x-mark" variant="link" color="primary" size="xl"
                @click.stop="removeActor(index)" />
            </UBadge>
          </div>
        </template>
      </USelectMenu>
    </div>

    <!-- Favorite movie -->
    <div class="flex flex-col">
      <label class="text-2xl font-medium">Your favorite director</label>
      <USelectMenu v-model="selectedMovies" :options="movieOptions" multiple placeholder="Select directors"
        class="mt-2">
        <template #default>
          <div class="flex flex-wrap gap-2 p-3 rounded-lg">
            <UBadge v-for="(movie, index) in selectedMovies" :key="index"
              class="bg-orange-400 text-lg text-white flex items-center gap-1 px-3 mx-2 py-1 rounded-full">
              {{ movie }}
              <UButton icon="i-heroicons-x-mark" variant="link" color="primary" size="xl"
                @click.stop="removeMovie(index)" />
            </UBadge>
          </div>
        </template>
      </USelectMenu>
    </div>

  </div>
</template>
