<script setup lang="ts">
import { useActors } from '~/composables/useActors'
import { useUserStore } from '~/store/userStore'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()
const { displayedActors, selectedActors, toggleActor, searchQuery } = useActors()

// 🔹 Vérification de l'authentification (middleware)
definePageMeta({
  middleware: 'auth',
  layout: 'auth'
})

// 🔹 Envoi des acteurs sélectionnés au backend et redirection
async function submitSelection() {
  console.log('Acteurs sélectionnés :', selectedActors.value)

  try {
    // await fetch('http://localhost:8000/api/users/favorite-actors', {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //     Authorization: `Bearer ${userStore.token}`
    //   },
    //   body: JSON.stringify({ userId: userStore.user?.id, actors: selectedActors.value.map(a => a.id) })
    // })

    router.push('/dashboard') // 🔹 Redirection vers l'étape suivante
  } catch (error) {
    console.error('Erreur lors de l\'envoi des acteurs sélectionnés:', error)
  }
}
</script>

<template>
  <div class="min-h-screen bg-black text-white flex flex-col p-12">
    <!-- 🔹 Titre -->
    <h1 class="flex justify-center mt-10 text-5xl font-extrabold text-left text-white mb-6">Select your favorite
      actor/actress</h1>

    <!-- 🔹 Barre de recherche -->
    <UInput v-model="searchQuery" placeholder="Search actors..." :ui="{ base: 'text-lg p-4' }"
      class="w-2/3 text-2xl p-5 mt-10 mx-auto bg-gray-800 text-black rounded-2xl shadow-lg" />

    <!-- 🔹 Sélectionnés en haut -->
    <div v-if="selectedActors.length" class="grid grid-cols-6 gap-6 mt-8">
      <div v-for="actor in selectedActors" :key="actor.id">
        <UButton @click="toggleActor(actor)"
          class="w-48 h-15 flex items-center justify-center rounded-2xl bg-orange-400 text-white shadow-xl hover:bg-orange-400"
          trailing-icon="mdi-close">
          <span class="text-xl font-semibold">{{ actor.name }}</span>
        </UButton>
      </div>
    </div>

    <!-- 🔹 Grille des acteurs -->
    <div class="grid grid-cols-6 gap-10 mt-12">
      <div v-for="actor in displayedActors.slice(0, 12)" :key="actor.id">
        <UButton @click="toggleActor(actor)"
          class="w-48 h-48 flex flex-col items-center justify-center rounded-2xl text-white shadow-xl hover:bg-orange-400 transition-all"
          :class="selectedActors.some(a => a.id === actor.id) ? 'bg-orange-400  border-orange-500' : ''">
          <img :src="actor.profilePath || '/placeholder.webp'" class="w-28 h-28 rounded-full object-cover"
            alt="Actor image" />
          <span class="mt-2 text-xl font-semibold">{{ actor.name }}</span>
        </UButton>
      </div>
    </div>

    <!-- 🔹 Bouton "Continue" -->
    <div class="flex justify-center mt-16">
      <UButton @click="submitSelection"
        class="flex justify-center w-52 py-4 text-2xl bg-orange-500 hover:bg-orange-600 text-white rounded-2xl shadow-xl transition-all">
        Continue →
      </UButton>
    </div>
  </div>
</template>