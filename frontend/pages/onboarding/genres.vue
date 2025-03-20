<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function finishOnboarding() {
  router.push('/') // 🔹 Redirection vers l'accueil après l'onboarding
}
</script>

<template>
  <div>
    <h1>Onboarding - Étape 3</h1>
    <button @click="finishOnboarding">Terminer</button>
  </div>
</template>