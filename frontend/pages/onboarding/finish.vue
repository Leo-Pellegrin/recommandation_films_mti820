<script setup lang="ts">
const router = useRouter()

function nextStep() {
  router.push('/')
}

definePageMeta({
  middleware: 'auth',
  layout: 'auth'
})
</script>

<template>
  <div>
    <h1>Onboarding - Étape 2</h1>
    <button @click="nextStep">Suivant</button>
  </div>
</template>