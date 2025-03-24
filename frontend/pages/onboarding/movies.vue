<script setup lang="ts">
import { useMovies } from '~/composables/useMovies'
// import { useUserStore } from '~/store/userStore'

// Vérification de l'authentification (middleware)
definePageMeta({
  middleware: 'auth',
  layout: 'auth'
})

const router = useRouter()
const { selectedMovies, toggleMovie, displayedMovies, searchQuery } = useMovies()

async function submitSelection() {
  console.log('Films sélectionnés :', selectedMovies.value)

  try {
    // TODO: Envoyer les films sélectionnés à l'API

    // await fetch('http://localhost:8000/api/users/favorite-movies', {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //     Authorization: `Bearer ${userStore.token}`
    //   },
    //   body: JSON.stringify({ userId: userStore.user?.id, movies: selectedMovies.value.map(a => a.id) })
    // })

    router.push('/onboarding/finish') //
  } catch (error) {
    console.error('Erreur lors de l\'envoi des films sélectionnés:', error)
  }
}

</script>

<template>
  <div class="min-h-screen bg-black text-white flex flex-col p-12">
    <h1 class="flex justify-center mt-10 text-5xl font-extrabold text-left text-white mb-6">Select your favorite
      movie</h1>

    
    <UInput v-model="searchQuery" placeholder="Search movies..." :ui="{ base: 'text-lg p-4' }"
      class="w-2/3 text-2xl p-5 mt-10 mx-auto bg-gray-800 text-black rounded-2xl shadow-lg" size="xl" />


    
    <div v-if="selectedMovies.length" class="grid grid-cols-6 gap-6 mt-8">
      <div v-for="movie in selectedMovies" :key="movie.id">
        <UButton @click="toggleMovie(movie)"
          class="w-48 h-15 flex items-center justify-center rounded-2xl bg-orange-400 text-white shadow-xl hover:bg-orange-400"
          trailing-icon="mdi-close">
          <span class="text-xl font-semibold">{{ movie.title }}</span>
        </UButton>
      </div>
    </div>


    
    <div class="grid grid-cols-6 gap-10 mt-12">
      <div v-for="movie in displayedMovies.slice(0, 12)" :key="movie.id">
        <UButton @click="toggleMovie(movie)"
          class="w-48 h-48 flex flex-col items-center justify-center rounded-2xl text-white shadow-xl hover:bg-orange-400 transition-all"
          :class="displayedMovies.some(a => a.id === movie.id) ? '  border-orange-500' : ''">
          <img :src="movie.posterPath || '/placeholder.webp'" class="w-28 h-28 rounded-xl object-cover"
            alt="Actor image" />
          <span class="mt-2 text-xl font-semibold">{{ movie.title }}</span>
        </UButton>
      </div>
    </div>

    <div class="flex justify-center mt-16">
      <UButton @click="submitSelection"
        class="mt-10 text-xl px-8 py-4 bg-orange-500 hover:bg-orange-600 text-white rounded-xl">
        Continue →
      </UButton>
    </div>

  </div>
</template>
