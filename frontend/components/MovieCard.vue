<template>
  <NuxtLink :to="`/movie/${id}`" :class="['relative overflow-hidden rounded-xl bg-gray-900 shadow-md', cardSizeClass]">
    <img :src="posterPath" :alt="title" :class="['w-full', imageHeightClass, objectFitClass]" />

    <div class="absolute bottom-0 left-0 w-full bg-black/30 p-2 text-white text-center text-lg font-semibold">
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
  size?: 'small' | 'medium' | 'large'
}>()

const cardSizeClass = computed(() => {
  switch (props.size) {
    case 'small': return 'w-[150px] h-[225px] min-w-[150px]'
    case 'medium': return 'w-[250px] h-[300px] min-w-[200px]'
    case 'large': return 'w-[300px] h-[450px] min-w-[250px]' // plus proche des dimensions réelles
    default: return 'w-[250px] h-[375px] min-w-[200px]'
  }
})

const imageHeightClass = computed(() => {
  switch (props.size) {
    case 'small': return 'h-[225px]'
    case 'medium': return 'h-[300px]'
    case 'large': return 'h-[450px]'
    default: return 'h-[375px]'
  }
})

const objectFitClass = computed(() => {
  return props.size === 'large' ? 'object-contain' : 'object-cover'
})
</script>ƒ