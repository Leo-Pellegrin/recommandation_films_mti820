<script setup lang="ts">
import { useAuth } from '#imports'

// Récupération de l'état d'authentification
const { status, data: session } = useAuth()
</script>

<template>
  <NuxtLayout>
    <template v-if="status === 'loading'">
      <div class="flex h-screen justify-center items-center">
        <span class="text-lg font-semibold">Loading...</span>
      </div>
    </template>

    <template v-else>
      <NuxtPage />
    </template>
  </NuxtLayout>
</template>