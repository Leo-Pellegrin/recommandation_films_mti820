<script setup lang="ts">
const router = useRouter()

function nextStep() {
  router.push('/onboarding/directors')
}
</script>

<template>
  <div>
    <h1>Onboarding - Étape 1</h1>
    <button @click="nextStep">Suivant</button>
  </div>
</template>