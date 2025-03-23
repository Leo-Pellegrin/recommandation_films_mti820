<script setup lang="ts">
const router = useRouter()

function goToHome() {
  router.push('/')
}
// 🔹 Vérification de l'authentification (middleware)
definePageMeta({
  middleware: 'auth',
  layout: 'auth'
})
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-screen  p-8">
    <div class="bg-gray-200 border border-gray-300 shadow-xl rounded-3xl p-12 max-w-2xl w-full text-center">
      <h1 class="text-5xl font-extrabold text-gray-800 mb-6">You're all set!</h1>
      <p class="text-2xl text-gray-600 mb-10">
        Your preferences have been saved. Get ready to discover personalized movie recommendations.
      </p>
      <UButton
        size="xl"
        class="bg-orange-400 hover:bg-orange-500 text-white font-bold text-2xl px-10 py-4 rounded-2xl"
        @click="goToHome"
      >
        Start Browsing →
      </UButton>
    </div>
  </div>
</template>