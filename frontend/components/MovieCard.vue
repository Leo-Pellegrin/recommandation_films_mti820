<template>
  <NuxtLink :to="`/movie/${id}`"
    class="relative w-[400px] h-[240px] min-w-[300px] mr-10 overflow-hidden rounded-xl bg-gray-900 shadow-md">
    <img :src="posterPath" :alt="title" class="object-cover w-full h-full" />
    <div class="absolute bottom-0 left-0 w-full bg-black/10 p-2 text-white text-center text-lg font-semibold">
      <p class="truncate">{{ title }}</p>
    </div>
  </NuxtLink>
</template>
<script setup lang="ts">
const props = defineProps<{
  id: number
  title: string
  posterPath: string
  rating?: number
}>()

</script>å√å