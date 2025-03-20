<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})
</script>

<template>
  <div>
    <h1>Bienvenue !</h1>
    <p>Si vous voyez ceci, vous êtes connecté.</p>
  </div>
</template>